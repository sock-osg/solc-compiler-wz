#!/usr/bin/python
import subprocess
import json
import sys

smartContractFile = sys.argv[1]
fullCommand = '/usr/local/bin/solc --add-std --optimize --combined-json abi,bin %s' % (smartContractFile)

def getScript():
  return """
  var contracts = contracts || {};
  %s contracts.deploy = function(a, b) {
    var c = web3.eth.contract(this[a].abi),
    d = c.new({
      from:eth.accounts[b],
      data:this[a].bin,
      gas:this[a].gas
      },function(b,c) {
        console.log(b, c), "undefined" != typeof c.address && console.log("Contract ["+a+"] mined! address: " + c.address + " transactionHash: " + c.transactionHash)
      });
    return d;
  };"""

def getContractScript():
  return 'contracts.%s = {"bin": "%s", "abi": %s, "gas": 4700000};'

def getAbiAndBytecode():
  p = subprocess.Popen(fullCommand.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = p.communicate()

  if err:
    print err
    sys.exit()

  return out.strip()

def parseJson(rawString):
  return json.loads(rawString)

def getContractsInformation(jsonResponse):
  contracts = {}
  for key in jsonResponse['contracts'].keys():
    smartContractInfo = jsonResponse['contracts'][key]
    contracts[key] = {'bin': '0x' + smartContractInfo['bin'], 'abi': smartContractInfo['abi']}
  return contracts

rawResponse = getAbiAndBytecode()
jsonResponse = parseJson(rawResponse)

contracts = getContractsInformation(jsonResponse)

contractsDefinitions = ''
for key in contracts.keys():
  contractsDefinitions += getContractScript() % (key, contracts[key]['bin'], contracts[key]['abi'])

scriptFilePath = smartContractFile.replace('.sol', '.js')

scriptFile = open(scriptFilePath , 'w')
scriptFile.write(getScript() % (contractsDefinitions))
scriptFile.close()

print "Execute in geth the following script: "
print "loadScript('%s')" % (scriptFilePath)
