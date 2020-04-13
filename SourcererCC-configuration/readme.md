Configuration
===

Step 1.
---
As mentioned in paper, we used `file-level` clone detection. the following changes were applied in configuration of SourcererCC.    
Go to `SourcererCC/tokenizers/file-level/` and in `config.ini`, replace:    
`File_extensions = .java`   
with:   
`File_extensions = .cpp`    
Then execute: `python tokenizer.py zip`  


Step 2.
---
Go to `SourcererCC/clone-detector/` and in `sourcerer-cc.properties`, replace:  
`DATASET_DIR_PATH=input/dataset`    
with the path of result files in tokenizing step ( or simply copy them to `input/dataset`)  
Then, replace:
```
MIN_TOKENS=65
MAX_TOKENS=500000
``` 
With:
```
MIN_TOKENS=1
MAX_TOKENS=250000
```
Then, go to `SourcererCC/clone-detector/` and in `runnodes.sh`, replace:    
`threshold="${3:-8}"`   
With:   
`threshold="${3:-10}"`  

Then run the clone detection as documented.
