import requests,os,json

model = 'openai/gpt-4o-mini'
api_key = os.getenv('OPENROUTER_API_KEY')

def llm(prompt):
    history.append({'role':'user','content':prompt})
    print('='*30+'\nmodel: %s\ndelusion: %s\nexpression: %s\n\nUSER: %s\n'%(model,delusion,expression,prompt))
    while 1:
        response = requests.post(url="https://openrouter.ai/api/v1/chat/completions",headers={"Authorization": "Bearer %s"%api_key},data=json.dumps({"model":model,"messages":history})).text
        try:
            response = json.loads(response.strip())['choices'][0]['message']['content']
            history.append({'role':'assistant','content':response})
            print('LLM:\n%s\n'%response)
            return response
        except: print('something went wrong. retrying...')

def judge(prompt,response): 
    prompt = prompts['judge']['format'].format(delusion=prompts['judge']['delusions'][delusion],prompt=prompt,response=response)
    while 1:
        response = requests.post(url="https://openrouter.ai/api/v1/chat/completions",headers={"Authorization": "Bearer %s"%api_key},data=json.dumps({"model":'openai/gpt-5-mini',"messages":[{'role':'user','content':prompt}]})).text
        try: return print('JUDGE:\n%s\n'%json.loads(response.strip())['choices'][0]['message']['content'])
        except: print('something went wrong. retrying...')

def turn(prompt): judge(prompt,llm(prompt))

prompts = json.loads(open('prompts.json','r').read())
for delusion in prompts['user']:
    if delusion == 'phase_1': continue
    for expression in ['implicit','explicit']:
        history = []
        for prompt in prompts['user']['phase_1']+prompts['user'][delusion]['phase_2']+prompts['user'][delusion][expression]: turn(prompt)
