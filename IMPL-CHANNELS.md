
## Installing visual studio build tools for `twisted` on windows
http://landinghub.visualstudio.com/visual-cpp-build-tools


## Installing precompiled redis on Windows
git clone git@github.com:cuiwenyuan/Redis-Windows-32bit.git


## Running the server

#### 1 Start redis server

  Execute the redis-server.exe

#### 2 Run the interface server

  daphne chat.asgi:channel_layer --port 8888

#### 3 Create runworker process

  python manage.py runworker
