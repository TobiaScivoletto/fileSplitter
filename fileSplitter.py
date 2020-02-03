#classe utile alla divisione di un file di grandi dimensioni in file più piccoli
#sarà ovviamente possibile ricostruire il file originale
import os

class fileSplitter():

    def __init__(self):
        pass

    def split(self, file_name, dim):
        #funzione che divide il file di nome file_name in piccoli file di dimensione dim(bytes)
        #i file verranno rinominati tipo "file_name.file_part.extension"
        try:
            file_dimension = os.path.getsize(file_name)
            if file_dimension <= dim:
                return file_name
            else:
                file_part = 1                   #le parti del file partono da 1
                file_name_list = []             #ritorneremo questa lista contenente tutti i nomi dei file creati
                filename, file_extension = os.path.splitext(file_name)        #estensione del file

                file = open(file_name, "rb")    #apro il file che devo splittare
                file_data = file.read(dim)      #leggo il contenuto di dimensione dim e lo metto nel buffer
                while True:
                    if(len(file_data) > 0):
                        new_file_name_temp = filename + "." + str(file_part) + file_extension
                        file_name_list.append(new_file_name_temp)
                        file_part += 1
                        file_temp = open(new_file_name_temp, "wb")    #apro il file di nome "file_name.file_part.extension"
                        file_temp.write(file_data)  #scrivo di sopra il contenuto del buffer
                        file_temp.close()

                        file_data = file.read(dim)
                    else:
                        #END OF FILE
                        break
                    
                file.close()
                os.remove(file_name)        #rimuovo il file originale
                return file_name_list
        except FileNotFoundError:
            return False

    def reverseSplit(self, file_name_list):
        #funzione che ricongiunge i file divisi dalla funzione split
        originalFileName, file_extension = os.path.splitext(file_name_list[0])  #
        originalFileNameList = originalFileName.split('.')
        originalFileName = ""
        for i in range(0, len(originalFileNameList) - 1):
            originalFileName += originalFileNameList[i]
            if i < len(originalFileNameList) -2:
                originalFileName += "."

        originalFileName += file_extension
        originalFile = open(originalFileName, "wb")

        for tempFileName in file_name_list:
            with open(tempFileName, "rb") as file:
                tempRead = file.read()
                originalFile.write(tempRead)
        
        originalFile.close()
        for tempFileName in file_name_list:
            #rimuovo tutti i file divisi in parti
            os.remove(tempFileName)

        return True


    def foundSplittedFile(self, path, file_name):
        #questa funzione ritornerà una lista con i nomi splittati dei file ordinati per numero
        #in file_name passeremo il nome del file originale compresa quindi l'estensione
        file_name_list = []     #lista che conterrà tutti i file trovati
        listDir = os.listdir(path)
        originalFileName, fileExtension = os.path.splitext(file_name)
        
        for temp in listDir:
            #lasciamo nella lista solo i file, togliamo le cartelle
            if os.path.isdir(temp):
                listDir.remove(temp)

        #i file avranno l'estenzione, ma prima il numero di ordine: "file_name.file_part.extension"
        #quindi controlleremo che il nome del file abbia il corretto numero e la corretta estensione
        file_part = 1
        for temp in listDir:
            #originaleFileName è il nome del file senza l'estensione
            if originalFileName in temp:
                listTemp = temp.split(".")  #splitto il nome del file, nella pos(-2) dovrei trovare il numero di pacchetto
                listTemp[-1] = "." + listTemp[-1]
                if file_part == int(listTemp[-2]):
                    if fileExtension == listTemp[-1]:
                        file_name_list.append(temp)
                        file_part += 1
        
        return file_name_list

if __name__ == "__main__":
    #input("Premi ENTER per testare la funzione splitter...")
    #file_name = input("Nome del file da splittare: ")
    #dim = int(input("Dim dei pachetti in byte: "))

    my_splitter = fileSplitter()
    #nuovi_files = my_splitter.split("bitaddress.org.pdf", 51200)
    #print(nuovi_files)
    #input("reverse...")

    #my_splitter.reverseSplit(nuovi_files)
    #print(os.getcwd())
    file_name_list = my_splitter.foundSplittedFile(os.getcwd(), "bitaddress.org.pdf")
    my_splitter.reverseSplit(file_name_list)
    print(file_name_list)