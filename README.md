# btrfstm

## Introduction
btrfstm is a tool to manage btrfs subvolume snapshots, it

1. Creates subvolume snapshots, and
2. Delete out of date snapshots.

## Installation

```
$ python3 setup.py install
```

## Usage

### Crontab

(not tested yet)

Keep Hourly snapshots for 3 days.
```
0 * * * * /usr/local/bin/btrfstm --working-dir=/data --name=dropbox --snapshot-prefix=hourly --count=72
```

Keep Daily snapshots for a month.
```
0 2 * * * /usr/local/bin/btrfstm --working-dir=/data --name=dropbox --snapshot-prefix=daily --count=31
```

Keep Monthly snapshots forever!
```
0 2 1 * * /usr/local/bin/btrfstm --working-dir=/data --name=dropbox --snapshot-prefix=monthly
```
