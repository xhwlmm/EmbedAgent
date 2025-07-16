root_path=your path to model dir

docker run --gpus all -it \
    --name embedeval_env \
    -v "${root_path}/code_and_dataset:/code_and_dataset" \
    -d \
    embedeval \