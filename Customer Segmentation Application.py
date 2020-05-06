import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename, asksaveasfilename, asksaveasfile

class Customer_Segmentation:

    def __init__(self, parent):

        self.parent = parent
   
        self.text = tk.Text(self.parent)
        self.text.pack()        
        
        self.b2 = tk.Button(self.parent, text='LOAD DATA', command=self.load, fg='red',font=("Times", 10))
        self.b2.pack()

        # Title
        self.canvas1 = tk.Canvas(self.parent, width = 100, height = 100,  relief = 'raised')
        self.canvas1.pack()
        
        # create buttons
        self.label2 = tk.Label(self.parent, text="Categorical Features. Seperated by space. Like: Var1 Var2")
        self.label2.config(font=('times', 10)) # configuration of the text and font
        self.canvas1.create_window(50, 10, window=self.label2  ) 
       
        self.entry1 = tk.Entry (self.parent,bd=3) 
        self.canvas1.create_window(50, 30, window=self.entry1)
        
        self.b3 = tk.Button(self.parent, text='Step 1: Run for encoding', command=self.Encoding)
        self.b3.pack()      
        self.b4 = tk.Button(self.parent, text='Step 2: Run Algorithm: Customer Segmentation', command=self.kmeans)
        self.b4.pack() 
        self.b5 = tk.Button(self.parent, text='Step 3: Save Result', command=self.save)
        self.b5.pack()


        
 ################################  
  
    
    def Encoding(self):
        self.text.insert(tk.END,str('Needed to be Encoded: '+ str(self.entry1.get()))+'\n \n')
        #Encoding
        from sklearn import preprocessing
        label_encoder = preprocessing.LabelEncoder()    
        variableencode=self.entry1.get().split(" ", len(self.entry1.get()))
        for item in self.df[variableencode]:
            self.df[item]=label_encoder.fit_transform(self.df[item])
        self.df1=self.df

    def kmeans(self):
        from sklearn.metrics import silhouette_score
        from sklearn.cluster import KMeans
        sil = []
        kmax = 10
        for k in range(2, kmax+1):
            kmeans = KMeans(n_clusters = k).fit(self.df1)
            labels = kmeans.labels_
            sil.append(silhouette_score(self.df1, labels, metric = 'euclidean'))
      
        kmeansmodel = KMeans(n_clusters= sil.index(max(sil)), init='k-means++', random_state=0)
        y_kmeans= kmeansmodel.fit_predict(self.df1)
        self.df1['Cluster']=y_kmeans
        self.text.insert(tk.END, str(self.df1.head(4))+ '\n \n') 
        self.text.insert(tk.END, str('Number of clusters:'+ str(sil.index(max(sil)))) +'\n')  

 ################################3   
    def load(self):

        name = askopenfilename(filetypes=[('CSV', '*.csv',), ('Excel', ('*.xls', '*.xlsx'))])

        if name:
            if name.endswith('.csv'):
                self.df = pd.read_csv(name)

            else:
                self.df = pd.read_excel(name)

            self.filename = name
        
        colnames=self.df.columns
        self.text.insert(tk.END, str(pd.DataFrame(colnames,columns=['Varaibels and Features'])) +'\n \n')   
        self.text.insert(tk.END, str("Which Features are in Categorical form? Please fill the appropriate box.")+'\n\n') 
        
    def save(self):
        import os
        
        formats=[('CSV', '*.csv'), ('Excel','*.xls'),('Excel', '*.xlsx')]
        export_output = asksaveasfilename(filetypes=formats,defaultextension='.csv',title='Output')
        
        if export_output.endswith('.csv'):
            self.df1.to_csv (export_output, index = False, header=True)
        if export_output.endswith('.xls') or export_output.endswith('.xlsx'):
            self.df1.to_excel (export_output, index = False, header=True)

 
root = tk.Tk()
root.title("Customer Segmentation Analysis")
root.geometry("700x700+400+5") # 700x700 sets the size of window. 400+5: position of window
top = Customer_Segmentation(root)
root.mainloop()   
    