## Work
- Presentation Docker

## Documents

## Code

- select doms from config values
- config --> choose to run not all phases ?
- all comments in english
- db --> phase 2 connection to domine !!!
- test phase 3,4,5
- Identify other multiprocess points

## Questions

- line 358 : 3_F1 countScoreInteraction.py 
    
    --> newDomBact = getExistAutresDomaines("PF11509") ==> Why ???
    
- STOP THAT

        text_file = open(self.temp_file_pseqs, "w")
        text_file.write(sequence)
        text_file.close()
        
        
29	lcl|CP014196.1_prot_AUT26_14840_2907	gene_92|GeneMark.hmm|554_aa|+|54970|56634	1	0	18
        
docker exec -it inphinity-database mysql -h phage_bact -u admin -proot -e "use phage_bact; select DomainAcc from PROTDOM where ProtId='lcl|CP014196.1_prot_AUT26_14840_2907' limit 10"
+-----------+
| DomainAcc |
+-----------+
| --PF00270 |
| PF04851   |
| PF00271   |
| PF03880   |
+-----------+

docker exec -it inphinity-database mysql -h phage_bact -u admin -proot -e "use phage_bact; select DomainAcc from PROTDOM where ProtId='gene_92|GeneMark.hmm|554_aa|+|54970|56634' limit 10"
+-----------+
| DomainAcc |
+-----------+
| PF00004   |
| PF08495   |
| --PF00271 |
| PF00176   |
| PF04851   |
+-----------+

docker exec -it inphinity-database mysql -h phage_bact -u admin -proot -e "use phage_bact; SELECT * from domine.INTERACTION WHERE Domain1='PF00270' and Domain2='PF00271';"
+---------+---------+-------+------+------+------+--------+--------+------+------+------+------+------+--------+--------+----------+------+----------------------+--------+
| Domain1 | Domain2 | iPfam | 3did | ME   | RCDP | Pvalue | Fusion | DPEA | PE   | GPE  | DIPD | RDFF | KGIDDI | INSITE | DomainGA | PP   | PredictionConfidence | SameGO |
+---------+---------+-------+------+------+------+--------+--------+------+------+------+------+------+--------+--------+----------+------+----------------------+--------+
| PF00270 | PF00271 |     1 |    1 |    1 |    0 |      0 |      1 |    0 |    0 |    1 |    1 |    0 |      0 |      0 |        0 |    0 | HC                   |      0 |
+---------+---------+-------+------+------+------+--------+--------+------+------+------+------+------+--------+--------+----------+------+----------------------+--------+


