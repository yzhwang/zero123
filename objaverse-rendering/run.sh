nohup python scripts/multi_process.py \
	--gpu 0 \
	--input_models_path /mnt/aiops/common/digital-twin/objaverse/split_file_new_1.json \
    --concurrent_blenders 8 > /dev/null 2>&1 &

nohup python scripts/multi_process.py \
	--gpu 1 \
	--input_models_path /mnt/aiops/common/digital-twin/objaverse/split_file_new_2.json \
    --concurrent_blenders 8 > /dev/null 2>&1 &

nohup python scripts/multi_process.py \
	--gpu 2 \
	--input_models_path /mnt/aiops/common/digital-twin/objaverse/split_file_new_3.json \
    --concurrent_blenders 8 > /dev/null 2>&1 &

nohup python scripts/multi_process.py \
	--gpu 3 \
	--input_models_path /mnt/aiops/common/digital-twin/objaverse/split_file_new_4.json \
    --concurrent_blenders 8 > /dev/null 2>&1 &

nohup python scripts/multi_process.py \
	--gpu 4 \
	--input_models_path /mnt/aiops/common/digital-twin/objaverse/split_file_new_5.json \
    --concurrent_blenders 8 > /dev/null 2>&1 &

nohup python scripts/multi_process.py \
	--gpu 5 \
	--input_models_path /mnt/aiops/common/digital-twin/objaverse/split_file_new_6.json \
    --concurrent_blenders 8 > /dev/null 2>&1 &

nohup python scripts/multi_process.py \
	--gpu 6 \
	--input_models_path /mnt/aiops/common/digital-twin/objaverse/split_file_new_7.json \
    --concurrent_blenders 8 > /dev/null 2>&1 &

nohup python scripts/multi_process.py \
	--gpu 7 \
	--input_models_path /mnt/aiops/common/digital-twin/objaverse/split_file_new_8.json \
    --concurrent_blenders 8 > /dev/null 2>&1 &
