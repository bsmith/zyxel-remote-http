# Cookbook of examples

```shell
export ZYXEL_HOST=172.16.X.Y
export ZYXEL_USER=admin
export ZYXEL_PASS=1234
export ZYXEL_FWVER=260
```

## Check login works

```shell
./zyxel-tool.py --host $ZYXEL_HOST --user $ZYXEL_USER --password $ZYXEL_PASS --fwversion $ZYXEL_FWVER login
```

This simply outputs `ok` or `fail`.

## Download config/logs

Using the cmd subcommand:

```shell
./zyxel-tool.py --host $ZYXEL_HOST --user $ZYXEL_USER --password $ZYXEL_PASS --fwversion $ZYXEL_FWVER --verbose cmd --cmd 5901 --show-form --form-field type=8 --form-field upmethod=1 --submit-form --save-response type_8.out
```

NB. valid types are 1,2,3,6,7,8, and are described by the `--show-form`.

| type | description |
| --- | --- |
| 1 | Running configuration |
| 2 | Startup configuration |
| 3 | Backup configuration  |
| 6 | Flash log             |
| 7 | Buffer log            |
| 8 | Tech Support          |

## Ping

Using the ping subcommand:

```shell
./zyxel-tool.py --host $ZYXEL_HOST --user $ZYXEL_USER --password $ZYXEL_PASS --fwversion $ZYXEL_FWVER --verbose ping --ip 172.16.X.Z --count 5 --size 1600
```

Using the cmd subcommand:

```shell
./zyxel-tool.py --host $ZYXEL_HOST --user $ZYXEL_USER --password $ZYXEL_PASS --fwversion $ZYXEL_FWVER cmd --cmd 530 --form-field ip=172.16.X.Z --show-form --submit-form --verbose
```

## MAC Table

Using the cmd subcommand:

```shell
./zyxel-tool.py --host $ZYXEL_HOST --user $ZYXEL_USER --password $ZYXEL_PASS --fwversion $ZYXEL_FWVER cmd --cmd 2049 --extract-table
```
