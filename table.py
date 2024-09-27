import tkinter as tk
import json


def add_to_data(text):
    try:
        with open('input.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
        
    data.append({text:0})
    
    
    with open("input.json",'w') as file:
        json.dump(data,file)
                

def get_value(value):
    with open("input.json",'r') as file:
        key = None
        data = json.load(file)
        listik = data[-1].keys()
        for i in listik:
            key = i
                
        data[-1][key] = value
                
    with open('input.json', 'w') as file:
        json.dump(data,file)
   
def get_max():        
    with open('input.json', 'r') as file:
        data = json.load(file)
            
    max_score = 0
            
    for player_dict in data:
        player_name = list(player_dict.keys())[0]
        
            
        player_score = player_dict[player_name]       
        if player_score > max_score:
            max_score = player_score
    
    max_score_name = None
    
    for player_dicti in data:
        for k,v in player_dicti.items():
            if v == max_score:
                max_score_name = k 
            
    return max_score_name,max_score        
    

           


def submit_text(entry,root):
    text = entry.get()
    add_to_data(text)
    root.destroy()

   
    
      
        


def main():    
    root = tk.Tk()
    root.title('Таблица лидеров')

    entry = tk.Entry(root, width = 50)
    entry.pack(pady=10)
    
    

    submit_button = tk.Button(root, text = 'Отправить',command = lambda:submit_text(entry,root))
    submit_button.pack()


        
    

    root.mainloop()

