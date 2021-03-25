# window10安装z3-solver python版本
- **注意pip安装的是z3-solver，而不是z3。**
## 步骤
### 方法1：使用pip安装z3（错误）
```bash
# 安装
pip install z3

# 测试
z3 -h

usage: z3 [-h] [--s3-prefix S3_PREFIX] [--filesystem FILESYSTEM]
          [--snapshot-prefix SNAPSHOT_PREFIX]
          {backup,restore,status} ...

list z3 snapshots

positional arguments:
  {backup,restore,status}
                        sub-command help
    backup              backup local zfs snapshots to an s3 bucket
    restore             not implemented
    status              show status of current backups

optional arguments:
  -h, --help            show this help message and exit
  --s3-prefix S3_PREFIX
                        S3 key prefix, defaults to z3-backup/
  --filesystem FILESYSTEM, --dataset FILESYSTEM
                        the zfs dataset/filesystem to operate on
  --snapshot-prefix SNAPSHOT_PREFIX
                        Only operate on snapshots that start with this prefix.
                        Defaults to zfs-auto-snap:daily.
```
### 方法1：使用pip安装z3-solver（正确）
```bash
pip install z3-solver
```
#### 测试-python文件运行

- 输入xx.python

```python
from z3 import *

if __name__ == "__main__":
    x, y, z = Ints('x y z')
    s = Solver()
    s.add(2 * x + 3 * y + z == 6)
    s.add(x - y + 2 * z == -1)
    s.add(x + 2 * y - z == 5)
    # 解方程=>  x = 2, y = 1, z = -1
    # 2x + 3y + z = 6
    # x - y + 2z = -1
    # x + 2y - z = 5
    print(s.check())  # sat
    print(s.model())  # [z = -1, y = 1, x = 2]
```

- 输出

```bash
sat
[z = -1, y = 1, x = 2]
```

- 输入：xx.python

```python
from z3 import *

if __name__ == "__main__":
    x = Int('x')
    s = Solver()
    a = 65537
    b = 64834
    c = 41958
    s.add(x > 0)
    s.add(x % a == b)
    s.add(x % b == c)

    print(s.check())  # sat
    print(s.model())  # [x = 227609298]
```

- 输出

```bash
sat
[x = 227609298]
```

