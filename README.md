Swap - Collaboraive Educator Marketplace
===============

About
-----------------
Swap (name TBD) is an web app to help teachers find, offload, and exchange supplies. Because teachers often have shifting needs, they end up having extra supplies or needing supplies that they don't have. We want to create an educator-only marketplace where teachers can swap supplies.

Getting up and running
-----------------
Swap is written in Python using the Django web framework. Postgres is used as a database.

In order to facilite cross-platform development, Docker is used to build and run the application and database. This means that you don't have to worry about installing Python, app dependencies, or a database on your local machine. All you need to have is Docker.

### What is Docker?
> Docker is a tool designed to make it easier to create, deploy, and run applications by using containers. Containers allow a developer to package up an application with all of the parts it needs, such as libraries and other dependencies, and ship it all out as one package. By doing so, thanks to the container, the developer can rest assured that the application will run on any other Linux machine regardless of any customized settings that machine might have that could differ from the machine used for writing and testing the code.
 
Source: [https://opensource.com/resources/what-docker](https://opensource.com/resources/what-docker)

### Installing Docker
Download the [Mac](https://store.docker.com/editions/community/docker-ce-desktop-mac) or [Windows](https://store.docker.com/editions/community/docker-ce-desktop-windows) installer and follow the installation insturctions.

Note that for Windows, Docker requires 64bit Windows 10 Pro, Enterprise, or Education, and Docker also requires that virtualization be enabled. Check out the [what to know before you install](https://docs.docker.com/docker-for-windows/install/#what-to-know-before-you-install) document for more info. It is competely possible to run Swap without Docker, and we can work on documentation and scripts to make that process easier if we have contributors who can't run Docker. Docker is just handy because it makes it so developers don't have to install or manage installations, and because it mimicks the production environment.

### Running the App
Open a terminal (Terminal on Mac, Command Prompt or PowerShell on Windows), navigate to the Swap directory, and run this command: `docker-compose up --build`.

This command will start the application in debug mode, a Postgres database instance, and nginx (a web server). Each of these runs in its own container, and you'll see output from the containers. Each line will start with the container name (e.g. `app_1`).

After the command has stopped generating output, you can view Swap app by going to [http://localhost](http://localhost) in your browser.

### Stoping the App
To shut down the Docker containers started by `docker-compose up`, you can simply press `Ctrl-C`/`Command-C`. This will shut down the containers and return you to the command prompt.

When you're making changes to Django files, the app will automatically restart so you can see you changes without shutting the Docker containers down. If Django encounters a fatal error, you will need to fix it and restart the containers.

Advanced Topics
-----------------
### Debugging via `pdb`
`pdb` is the Python debugger, and it provides a useful way to interact with a running program.

If you need to debug Swap Python code, add the following `import pdb; pdb.set_trace()` at the point where you would like your breakpoint. The app will stop execution when it reaches this line.

To interact with `pdb`, open a new terminal and run `docker-attach swap_app_1` (where `swap_app_1` is the name of the container you see when running `docker ps`).