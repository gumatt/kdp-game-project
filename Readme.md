# KDP Project


## Starting Litestar api server

```bash
# run from root direcdtory using litestar_app script
litestar --app litestar_api:api run --reload --port XXXX

# or

# run from root directory using kdp package apps module for litestar
litestar --app kdp.apps.litestar.api.app:app run --reload --port XXXX

# or set environment var KDP_APP=kdp.apps.litestar.api.app:app

litestar --app $KDP_APP run --reload --port XXXX

```

Note:  --reload is an option of the run command within litestar, and not an option of litestar itself.



### Default "Problems Pane" filter settings
```
kpd/**/*.py, tests/**/*,py
```