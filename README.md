## Environment
```bash
# build image
cd ./docker
docker build -t embedeval .
# run container
bash run_docker.bash
# enter container
docker exec -it embedeval_env /bin/bash
# start screen
Xvfb :99 -screen 0 1024x768x24 &
export DISPLAY=:99
```

## Evaluation
### preparation
1. Register an account on [Wokwi](https://wokwi.com/)
2. Find your user ID, go to wokwi.com in your browser and sign in. Open the developer console (press F12 on your keyboard) and go to the 'Storage' tab (on Firefox) or 'Application' tab (on Chrome/Edge). Select the dropdown for 'Local Storage' and choose 'https://wokwi.com/'. Find the 'wokwiUser' key on the right, then double-click the 'value' next to it (which should look like random letters and numbers) and copy+paste it.
3. copy your userID to `./wokwi/untils.py`:
```python
WOKWI_TEST_ID = 'your_user_id'
```
4. infer the model and save the result to `./dataset/infer_results`:
5. run the evaluation:
```bash
# create the projects and save the url file
cd ./wokwi
python 4_create_project.py \
    --num 127 \ # number of projects
    --task with_connection \ # the task to eval
    --lang c \ # create c and python projects
    --user_id # your user id


python 0_get_url_projects.py \
    --url_path \ # path to save the url file
    --user_id # your user id

------------------------------
# model inference
# for model
python -u 3_infer.py \
    --model_name ${model name} \
    --model_dir ${model dir} \
    --temperature ${temperature} \
    --max_tokens ${max_tokens} \
    --stop ${stop tokens} \
    --data_path ${embedeval path} \
    --task ${task name} \
    --platform ${platform name} \
    --total_data ${total number of projects} \
    --sample_indices ${sample indices for inference} \
    --output_dir ${output dir}

# for api
python -u 3_infer_api.py \
    --model_name ${model name} \
    --temperature ${temperature} \
    --max_tokens ${max_tokens} \
    --api_key ${api key} \
    --base_url ${base url} \
    --data_path ${embedeval path} \
    --task ${task} \
    --total_data ${total number of projects} \
    --sample_indices ${sample indices for inference} \
    --output_dir ${output dir}

------------------------------
python 5_update_project.py \
    --url_path # path to the url file
    --total_data # total number of projects
    --task  # the task to eval
    --correct_path # correct result
    --predict_path # predict result

python 6_compile_project.py \
    --url_path # path to the url file
    --root_path # path to the result of models
    --task  # the task to eval
    --model_name # model name
    --total_data # total number of projects
```
