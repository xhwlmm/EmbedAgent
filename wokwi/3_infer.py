from vllm import LLM, SamplingParams
import json
from transformers import AutoTokenizer
import argparse
from prompt import translate_prompt, generate_prompt
from untils import read_json, remove_annotation
from untils import TOT_DATA
import json
from tqdm import tqdm
import os

def gen_result(examples, tokenizer, llm, model: str):
    if "chat" in model:
        try:
            prompts = [
                tokenizer.apply_chat_template(ex["prompt"], tokenize=False, add_generation_prompt=True)
                for ex in examples
            ]
        except:
            prompts = [ex["prompt"][1]['content']+"\n###Response\n" for ex in examples]

    # Create a sampling params object.
        
    sampling_params = SamplingParams(
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        stop= None if args.stop == '' else args.stop
    )

    print("Sample prompt: {}".format(prompts[0]))
    outputs = llm.generate(prompts, sampling_params)
    for i in range(len(examples)):
        examples[i]['generation'] = outputs[i].outputs[0].text
    return examples

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, default='Qwen2.5-72B-Instruct')
    parser.add_argument('--model_dir', type=str, default='')
    parser.add_argument('--temperature', type=float, default=0)
    parser.add_argument('--max_tokens', type=int, default=8192)
    parser.add_argument('--stop', type=str, default='')
    parser.add_argument('--data_path', type=str, default='./dataset/prompt.jsonl')
    parser.add_argument('--task', type=str, default='without_connection', help='with_connection, without_connection, translate_platform_lang')
    parser.add_argument('--platform', type=str, default='Arduino Mega')
    parser.add_argument('--total_data', type=int, default=TOT_DATA)
    parser.add_argument('--sample_indices', type=int, nargs='+', default=None, help='List of sample indices to use (default: all indices)')
    parser.add_argument('--output_dir', type=str, default='./dataset/infer_results')

    args = parser.parse_args()
    
    if args.sample_indices is None:
        args.sample_indices = list(range(args.total_data))

    # create output dir
    os.makedirs(args.output_dir, exist_ok=True)
    model_name_or_path = f"{args.model_dir}/{args.model_name}"
    output_dir = f"{args.output_dir}/{args.model_name}"
    os.makedirs(output_dir, exist_ok=True)

    if os.path.exists(f"{output_dir}/{args.task}.json"):
        ds = read_json(f"{output_dir}/{args.task}.json")
    else:
        ds = read_json(args.data_path)

    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)

    # create an LLM.
    llm = LLM(
        model=model_name_or_path,
        pipeline_parallel_size=1,
        tensor_parallel_size=2,
        max_num_seqs=10,
        max_num_batched_tokens=args.max_tokens,
        max_model_len=args.max_tokens,
        gpu_memory_utilization=0.9,
        trust_remote_code=True
    )

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
    # gen result
    gen_res = gen_result(prompts,tokenizer,llm,"chat")

    for index, sample_index in enumerate(args.sample_indices):
        ds[sample_index]["response"] = gen_res[index]['generation']
                    
    with open(f"{output_dir}/{args.task}.json","w",encoding="utf-8") as f:
        json.dump(ds,f,indent=4,ensure_ascii=False)