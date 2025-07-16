import argparse
from untils import deepseek_api_key, hardware_id, deepseek_base_url
from untils import gpt_response, read_json
from prompt import problem_description
from tqdm import tqdm
import json
        
def main(args):
    # read data
    correct_data = read_json(args.correct_path)
    # read chinese problems
    # TODO optimize this part
    ch_problems = []
    for i in range(1,21):
        with open(f"./test/{i}.py", "r", encoding="utf-8") as f:
            code = f.read()
            code = code.split("\n")
            ch_problem = ""
            for line in code:
                if line.startswith("#"):
                    ch_problem += line[1:].strip() + "\n"
                elif line == "":
                    continue
                else:
                    break
            ch_problems.append(ch_problem)
    
    # generate prompt
    prompts = []
    for index, data in enumerate(correct_data):
        prompt = problem_description(
            ch_problems[index],
            data['sketch'],
            eval(data['diagram'])
        )
        prompts.append(prompt)
    # add hardware information
    for index, data in enumerate(correct_data):
        diagram = eval(data['diagram'])
        info = [0 for _ in range(8)]
        for hardware in diagram['parts']:
            hardware_type = hardware['type'].replace('wokwi-','')
            info[hardware_id[hardware_type]] += 1
        correct_data[index]['hardware'] = info
    # generate response
    for index in tqdm(range(len(prompts))):
        prompt = prompts[index]
        message = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
        ]
        response = gpt_response(
            message,
            args.api_key,
            args.base_url,
            {
                'model': args.model_name,
                'max_tokens': args.max_tokens,
                'temperature': args.temperature,
                'stop': args.stop
            }
        )
        correct_data[index]['problem'] = response.split('[English Description]')[1].strip()
    # save data
    with open(args.save_path, 'w', encoding='utf-8') as f:
        for data in correct_data:
            json.dump(data, f, ensure_ascii=False)
            f.write('\n')
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--correct_path', type=str, default='../dataset/correct.jsonl')
    parser.add_argument('--save_path', type=str, default='../dataset/prompt.jsonl')
    parser.add_argument('--temperature', type=float, default=0)
    parser.add_argument('--model_name', type=str, default='deepseek-chat')
    parser.add_argument('--max_tokens', type=int, default=1024)
    parser.add_argument('--stop', type=str, default='[/English Description]')
    parser.add_argument('--api_key', type=str, default=deepseek_api_key)
    parser.add_argument('--base_url', type=str, default=deepseek_base_url)
    args = parser.parse_args()
    
    main(args)