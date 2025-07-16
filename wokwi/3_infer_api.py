import json
from transformers import AutoTokenizer
import argparse
from prompt import translate_prompt, generate_prompt
from untils import read_json, remove_annotation,gpt_response
from untils import deepseek_base_url,deepseek_api_key,TOT_DATA
import json
from tqdm import tqdm
import os
import concurrent.futures

def process_single_example(i, examples, prompts, args):
    parameters = {
        'model': args.model_name,
        'max_tokens': args.max_tokens,
        'temperature': args.temperature,
        'stop': args.stop,
    }
        
    response = gpt_response(
        prompts[i], 
        args.api_key, 
        args.base_url,
        parameters
    )
    examples[i]['generation'] = response
    
    return i 

def gen_result(examples, args):
    prompts = [ex["prompt"] for ex in examples]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        futures = [
            executor.submit(
                process_single_example,
                i, examples, prompts, args
            )
            for i in range(len(examples))
        ]
        for _ in tqdm(
            concurrent.futures.as_completed(futures),
            total=len(futures),
            desc="Generating"
        ):
            pass
    process_single_example(0, examples, prompts, args)
    
    return examples

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, default='deepseek-chat')
    parser.add_argument('--temperature', type=float, default=0)
    parser.add_argument('--max_tokens', type=int, default=8192)
    parser.add_argument('--stop', type=str, default='')
    parser.add_argument('--api_key', type=str, default=deepseek_api_key)
    parser.add_argument('--base_url', type=str, default=deepseek_base_url)
    parser.add_argument('--data_path', type=str, default='./dataset/prompt.jsonl')
    parser.add_argument('--task', type=str, default='translate_Pi-Pico_micro-python', help='with_connection, without_connection, translate_platform_lang')
    parser.add_argument('--platform', type=str, default='Arduino Mega')
    parser.add_argument('--total_data', type=int, default=TOT_DATA)
    parser.add_argument('--sample_indices', type=int, nargs='+', default=None, help='List of sample indices to use (default: all indices)')
    parser.add_argument('--output_dir', type=str, default='./dataset/infer_results')

    args = parser.parse_args()

    if args.sample_indices is None:
        args.sample_indices = list(range(args.total_data))
    # create output dir
    os.makedirs(args.output_dir, exist_ok=True)
    cur_model_name = args.model_name.split("/")[-1]
    output_dir = f"{args.output_dir}/{cur_model_name}"
    os.makedirs(output_dir, exist_ok=True)
    if os.path.exists(f"{output_dir}/{args.task}.json"):
        ds = read_json(f"{output_dir}/{args.task}.json")
    else:
        ds = read_json(args.data_path)
    # gen prompt
    prompts = []
    for index,sample in enumerate(ds):
        if index not in args.sample_indices: continue
        solution = remove_annotation(sample["sketch"],'c')
        problem = sample["problem"]
        diagram = sample["diagram"][args.platform]
        hardware_lst = sample["hardware_lst"]
        if args.task.startswith("translate"):
            task = {"platform": args.task.split("_")[1], "language": args.task.split("_")[2]}
            cur_prompt = translate_prompt(solution,diagram,hardware_lst,args.platform,task)
        else:
            cur_prompt = generate_prompt(problem,diagram,hardware_lst,args.task,args.platform)
        if args.platform == "Arduino Mega":
            cur_prompt = cur_prompt.replace("uno","mega")
        message = [
            {"role": "system", "content": "You are an expert in embeded system design."},
            {"role": "user", "content": cur_prompt}
        ]
        prompts.append({"prompt":message})
    print(prompts[0]['prompt'][1]['content'])
    # gen result
    gen_res = gen_result(prompts,args)

    for index, sample_index in enumerate(args.sample_indices):
        ds[sample_index]["response"] = gen_res[index]['generation']
                    
    with open(f"{output_dir}/{args.task}.json","w",encoding="utf-8") as f:
        json.dump(ds,f,indent=4,ensure_ascii=False)