# Executions
## Ressources

### 29.11.2016

6 organismes + 25 sequences/organism ==> ~3min/hmmsearch run

6*25 = 150 sequences to analyse by hmmsearch container

Multiprocess pool = 10 --> We can almost divided by pool_size les executions. Not really true, because it 
treat sequences for one organism at a time.

~time = (150/10) * 3 = 45 minutes

##### Real Execution
\#1: 36m