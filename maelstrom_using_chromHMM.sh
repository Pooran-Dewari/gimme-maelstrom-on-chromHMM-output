[[ -z "$1" ]] && { echo "Please supply Experiment Name" ; return; }

[[ -z "$2" ]] && { echo "Please supply ATAC consensus filename" ; return; }

conda activate gimme
#first extract the active enhancer
ls *dense.bed | while read BED;
do
    echo "now extracting from $BED"
    cat $BED | awk '{ if ($4 == 6) print $1, $2, $3, $4}'  OFS='\t' > $BED"_Act_Enh.bed"
done

#merge active enhancer  bed files into one master bed file
bedops --merge  *_Act_Enh.bed > $1"_Act_Enh.bed"

#intersect ATAC peaks with Active Enhancer master bed file, save reports for ATAC file
bedtools intersect -a $2 -b $1"_Act_Enh.bed" -wa > $1"_for_gimme.bed"

#count tags using intersected ATAC peaks from above
bedtools multicov \
-bams Ss1_ATAC.bam.sort Ss2_ATAC.bam.sort Ss3_ATAC.bam.sort Ss4_ATAC.bam.sort Ss5_ATAC.bam.sort \
-bed $1"_for_gimme.bed" > $1"_tag_counts.tsv"



awk '{print $1":"$2"-"$3,$4,$5,$6,$7,$8}' OFS='\t'  $1"_tag_counts.tsv" \
 | awk 'BEGIN {OFS="\t"; print "", "Ss1", "Ss2", "Ss3", "Ss4", "Ss5"} {print $0}' \
 > $1"_tag_counts.tsv""_withHeader.tsv"


#run part1 of gimme maelstrom, i.e, make the tsv.gz file
python3.9 maelstrom.py  $1"_tag_counts.tsv""_withHeader.tsv"  $1

#now run part2 of gimme maelstrom
gimme maelstrom  $1".withHeader_tsv"".gz" Ssal_v3.1  $1".out" -p gimme.vertebrate.v5.0 -N 7


#make heatmap
python3.9  heatmap.py $1".out" heatmap

conda deactivate
