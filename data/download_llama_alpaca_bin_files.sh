

#!/bin/bash
for i in {1..9}
do
    wget https://huggingface.co/chainyo/alpaca-lora-7b/resolve/main/pytorch_model-0000$i-of-00039.bin
done

for i in {10..39}
do
    wget https://huggingface.co/chainyo/alpaca-lora-7b/resolve/main/pytorch_model-000$i-of-00039.bin
done

