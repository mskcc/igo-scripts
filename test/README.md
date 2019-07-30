# Tests for Nikon Single Cell Scripts 

## Nikon Renaming Script
Note - This test script creates two directories to mock the Nikon directory images are created in and the directory they are moved to. See below.
```
$ python3 test_igo_transfer.py 
..Creating igo dir at /Users/streidd/work/igo-scripts/test/Transfer_test
Creating nikon dir at /Users/streidd/work/igo-scripts/test/igo_dir_test
Finished setup
Creating mock nikon files
Finished creating mock nikon files
Starting transfer from /Users/streidd/work/igo-scripts/test/Transfer_test to /Users/streidd/work/igo-scripts/test/igo_dir_test
Transferred 10368 files to /Users/streidd/work/igo-scripts/test/igo_dir_test
Verifying file contents of dir: /Users/streidd/work/igo-scripts/test/igo_dir_test
.
----------------------------------------------------------------------
Ran 3 tests in 5.975s

OK
lski2780:test streidd$ `
$ tree -d
.
├── Transfer_test
└── igo_dir_test
    ├── c1
    │   └── S0000
    │       ├── C01
    │       ├── C02
    │       ├── C03
    │       ├── C04
    │       ├── C05
    │       ├── C06
    │       ├── C07
    │       ├── C08
    │       ├── C09
    │       ├── C10
    │       ├── C11
    │       ├── C12
    │       ├── C13
    │       ├── C14
    │       ├── C15
    │       ├── C16
    │       ├── C17
    │       ├── C18
    │       ├── C19
    │       ├── C20
    │       ├── C21
    │       ├── C22
    │       ├── C23
    │       ├── C24
    │       ├── C25
    │       ├── C26
    │       ├── C27
    │       ├── C28
    │       ├── C29
    │       ├── C30
    │       ├── C31
    │       ├── C32
    │       ├── C33
    │       ├── C34
    │       ├── C35
    │       ├── C36
    │       ├── C37
    │       ├── C38
    │       ├── C39
    │       ├── C40
    │       ├── C41
    │       ├── C42
    │       ├── C43
    │       ├── C44
    │       ├── C45
    │       ├── C46
    │       ├── C47
    │       ├── C48
    │       ├── C49
    │       ├── C50
    │       ├── C51
    │       ├── C52
    │       ├── C53
    │       ├── C54
    │       ├── C55
    │       ├── C56
    │       ├── C57
    │       ├── C58
    │       ├── C59
    │       ├── C60
    │       ├── C61
    │       ├── C62
    │       ├── C63
    │       ├── C64
    │       ├── C65
    │       ├── C66
    │       ├── C67
    │       ├── C68
    │       ├── C69
    │       ├── C70
    │       ├── C71
    │       └── C72
    └── c2
        └── S0000
            ├── C01
            ├── C02
            ├── C03
            ├── C04
            ├── C05
            ├── C06
            ├── C07
            ├── C08
            ├── C09
            ├── C10
            ├── C11
            ├── C12
            ├── C13
            ├── C14
            ├── C15
            ├── C16
            ├── C17
            ├── C18
            ├── C19
            ├── C20
            ├── C21
            ├── C22
            ├── C23
            ├── C24
            ├── C25
            ├── C26
            ├── C27
            ├── C28
            ├── C29
            ├── C30
            ├── C31
            ├── C32
            ├── C33
            ├── C34
            ├── C35
            ├── C36
            ├── C37
            ├── C38
            ├── C39
            ├── C40
            ├── C41
            ├── C42
            ├── C43
            ├── C44
            ├── C45
            ├── C46
            ├── C47
            ├── C48
            ├── C49
            ├── C50
            ├── C51
            ├── C52
            ├── C53
            ├── C54
            ├── C55
            ├── C56
            ├── C57
            ├── C58
            ├── C59
            ├── C60
            ├── C61
            ├── C62
            ├── C63
            ├── C64
            ├── C65
            ├── C66
            ├── C67
            ├── C68
            ├── C69
            ├── C70
            ├── C71
            └── C72

150 directories
```
