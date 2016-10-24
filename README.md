# Usage
```
./compiler-wizard smart-contract-name.sol
```

# Load generated script

This wizard creates a .js file which you can attach into geth. You need to execute the function *loadScript*.

Once the scrip is loaded, you will have access to the object *contracts*, which contains all the information of the smart contract
binary build, included ABI Interface.
