# tot
CLI to manage the corrections workflow of the subject Computers and related subjects in the URV

# Argument behaviour
Default arguments can be customized via (from less to more priority) 
system variables, global configuration file, specific configuration file of the 
repo, specific
configuration file for the execution.


# Components


# CLI modules
## tot run
This module runs NDS binaries using different backends. 

(If possible, depending on the backend) this module features the exit of the runner process if the main function of the 
binary reached its end, which is useful 
when testing NDS software.

### Mandatory arguments
A valid NDS binary file must be provided for the module to run. This information can be supplied or assumed in different
ways.

With no arguments, this module runs the first `.nds` file found in the directory where `tot` is invoked. If 
there are more than one `.nds` file in that directory, shows a warning regarding the assumption made.

With `-f PATH/TO/NDS/file.nds` the NDS file to run can be provided with no assumptions. 

With `-d PATH/TO/DIR/WITH/NDS/FILES` the module will behave the same as with no arguments, but using the passed 
directory for finding the `.nds` files.

`-d` and `-f` can not be used together.

### Optional arguments
With `--image PATH/TO/FAT/file.fat` the module will load the FAT image as file into the runner if possible. 

With `-e` or `--environment docker|(host|bmde)|flatpak` you can choose what backend you are using to execute the NDS 
binary. 
* With `docker`
it uses the desmume-docker project to run the binary. Currently, this backend has no screen output, but it could be 
implemented in the future if the host has a VNC-compatible display server. The default entrypoint for this backend is 
`desmume-cli`
* With `host` uses the shell command `desmume` to run the binary, whatever is the implementation of the underlying 
binary. The default entrypoint for this backend is `desmume`.
* With `flatpak` uses the FlatPak implementation of DeSmuME. 

If not specified, the backend will be assumed depending on the presence of each backend in the system. If there are 
more than one possible backend, it will be chosen from the options, from more priority to less priority: `host`, 
`docker` and finally `flathub`.

When using the backends `host` and `docker`, the option 
`--entrypoint PATH/TO/ENTRYPOINT` is available, which allows to override the file executed as entrypoint.

When using the backend `docker`, the option `-s` or `--shell` can be used, which gives a shell inside
the Docker container
used for running the project.

All options after `--` will be passed to the underlying entrypoint if possible.

With `--debug`, the execution of the runner, if possible, starts with GDB stubs on and the runner waits for connection 
on port 1000.

With `-p` or `--port`, you can choose which port to expose for the debugger to connect. This assumes `--debug`.

If possible, the option `--dry-run` will be implemented to simulate what the program would do.

With `--verbose` shows more information and with `--trace` shows all logs. With `-q` shows no output.   


## tot build
This module compiles NDS projects using different backends as building environments.

### Mandatory arguments
A valid NDS project directory must be provided for the module to run. This information can be supplied or assumed in 
different
ways.

With no arguments, this module executes `make` in the directory where `tot` is invoked. 

With `-d PATH/TO/DIR/WITH/NDS/FILES` the module will behave the same as with no arguments, but using the passed 
directory as the directory where the NDS project to build is located.

### Optional arguments
With `-e` or `--environment docker|(host|bmde)` you can choose what backend you are using to build the NDS 
binary. 
* With `docker`
it uses the devkitarm-docker project to run the binary. 
* With `host` uses the shell command `desmume` to run the binary, whatever is the implementation of the underlying 
binary.

The default entrypoint for all backends is `make`.

The option 
`--entrypoint PATH/TO/ENTRYPOINT` is available, which allows to override the file executed as entrypoint.

When using the backend `docker`, the option `-s` or `--shell` can be used, which gives a shell inside
the Docker container
used for building the project.

All options after `--` will be passed to the underlying entrypoint if possible.

If possible, the option `--dry-run` will be implemented to simulate what the program would do.

With `--verbose` shows more information and with `--trace` shows all logs. With `-q` shows no output.   

## tot patch
This module patches NDS binaries so that they can access a FAT image.

### Mandatory arguments
A valid NDS binary must be provided for the module to run. This information can be supplied or assumed in 
different
ways.

With no arguments, this module patches the first `.nds` file found in the directory where `tot` is invoked. 

With `-f PATH/TO/DIR/WITH/NDS/file.nds` the module will behave the same as with no arguments, but using the passed 
file as the file to be patched. 

### Optional arguments
With `-e` or `--environment docker|(host|bmde)` you can choose what backend you are using to build the NDS 
binary. 
* With `docker`
it uses the devkitarm-docker project to run the binary. 
* With `host` uses the shell command `desmume` to run the binary, whatever is the implementation of the underlying 
binary.

The default backend is `docker`.

If possible, the option `--dry-run` will be implemented to simulate what the program would do.

With `--verbose` shows more information and with `--trace` shows all logs. With `-q` shows no output.   


## tot clean
Wrapper for `tot build -- clean`, to provide a handy way to clean the project artifacts. It has the same arguments as 
`tot build` with a fe differences.

All options after `--` will be passed after the clean command to the underlying entrypoint.

## tot git
This module wraps a custom pre-configured `git` environment.

This module features the possibility of being able to connect to a `forticlient` VPN inside the container, which is 
useful when connecting to `git` servers behind this type of VPN. It also features a bypass of the authentication prompt
from the `git` server using provided credentials, making the `git` process to execute non-interactive. 

### Mandatory arguments
Some of the mandatory arguments contain sensible data, they can only be provided 
via file or system variable. 

The file must have a key-value format (as in `.env` files). A file can be provided with the argument `-p` 
`--password-file 
PATH/TO/PASSWORD/FILE`. The file `.env` of the directory where `tot` is executed is always used.

The same keys that can be provided in the file, can be used with underscores and capital letters for providing the 
arguments via system variables. 

The priority to read the different values from more to less priority is: via `-p` argument, via `.env` file in the 
execution directory and system variables. The meaning, values and syntax for each argument in its possible sources are 
explained 
below.

You will need to provide the VPN details if you want the VPN on. The required VPN details are the following:
% TODO: complete details, defaults and structure with table
* VPN username | VPN_USERNAME | vpn-username
* VPN password  
* VPN host
* VPN port

You can provide the `git` user details to author the commits you make in the repository. The required `git` details are 
the 
following:
* git name
* git email

You will need to provide the `git` user credentials to be able to connect to the server. The required `git` credentials
are:
* git username
* git password
* git host


### Optional arguments
A valid `git` project directory could be provided to the module to run `git` commands inside it. This information can be 
supplied, or it will be assumed.

With no arguments, this module assumes as project directory the directory where `tot` is invoked. 

With `-d PATH/TO/DIR/WITH/NDS/FILES` the module will behave the same as with no arguments, but using the passed 
directory as the directory where the NDS project to build is located.

With `-e` or `--environment docker|(host|bmde)` you can choose what backend you are using to build the NDS 
binary. 
* With `docker`
it uses the `fortivpn-git-docker` project to run the binary. 
* With `host` uses the shell command `git` to run the binary, whatever is the implementation of the underlying 
binary.

The default entrypoint for all backends is `git`.

When using the backend `docker`, the option `-s` or `--shell` can be used, which gives a shell inside
the Docker container with the `git` environment.

All options after `--` will be passed to the underlying entrypoint.

If possible, the option `--dry-run` will be implemented to simulate what the program would do.

With `--verbose` shows more information and with `--trace` shows all logs. With `-q` shows no output.   

With `--vpn on|off` you can control the VPN. The default is `on`.

## tot clone REPO_NAME
Wrapper around `tot git -- clone GIT_USERNAME@GIT_HOST:REPO_NAME` that has the same arguments as `tot git`.

## tot edit
This module edits NDS projects using different backends as IDEs / editors.

### Mandatory arguments
A valid directory must be provided for the module to run. This information can be supplied or assumed in 
different
ways.

With no arguments, this module executes an IDE in the directory where `tot` is invoked. 

With `-d PATH/TO/DIR/WITH/NDS/PROJECT` the module will behave the same as with no arguments, but using the passed 
directory as the directory where the NDS project to build is located.

### Optional arguments
With `-e` or `--environment docker|(host|bmde)` you can choose what backend you are using to build the NDS 
binary. 
* With `docker`
it uses the vscode-docker project to edit the project.
* With `host` uses the shell command `vscode` to edit the project, whatever is the implementation of the underlying 
binary.

The default entrypoint for all backends is `vscode`.

The option 
`--entrypoint PATH/TO/ENTRYPOINT` is available, which allows to override the file executed as entrypoint.

All options after `--` will be passed to the underlying entrypoint if possible.

With `--verbose` shows more information and with `--trace` shows all logs. With `-q` shows no output.   

## tot debug

## tot validate


## tot lint

## tot prepare

## tot test





