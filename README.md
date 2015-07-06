# GogoBot

Gogolook Hipchat bot created using [err bot](https://github.com/gbin/err)

## Setup
1. clone [https://github.com/Gogolook-Inc/GogoBot](https://github.com/Gogolook-Inc/GogoBot)
2. go into directory `cd GogoBot`
2. create python virtual environment `virtualenv venv`
3. activate python virtual environment `source venv/bin/activate`
5. set flag or errbot will not be installed due to some " fatal error: 'ffi.h' file not found"
	`sudo bash`
	`export CFLAGS=-Qunused-arguments`
	`export CPPFLAGS=-Qunused-arguments`
	`export PKG_CONFIG_PATH=/usr/local/Cellar/libffi/3.0.13/lib/pkgconfig/`
4. install err `pip install err`
7. install sleekxmpp    `pip install sleekxmpp`
5. finally, run bot `err.py`


## Plugin Development
1. read this plugin development doc [https://github.com/gbin/err/wiki/plugin-dev](https://github.com/gbin/err/wiki/plugin-dev)
2. clone plugin template [https://github.com/zoni/err-skeleton](https://github.com/zoni/err-skeleton)
3. create folder in `plugins-dev` named `err-your_plugin_name`
4. start writing python code!


## Troubleshooting
- you might need to install libffi `brew install libffi`


## Roadmap
- lunch reminder
- jenkins integration
- unit tests [https://github.com/gbin/err/wiki/plugin-dev#testing-your-plugin](https://github.com/gbin/err/wiki/plugin-dev#testing-your-plugin)
- ~~restructure plugin directory~~
