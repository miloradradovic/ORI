import os
import shutil

def loadData():
    #print(os.listdir("C:/Users/Vukasin/Desktop/chest_xray_data_set/chest_xray_data_set/IM-0689-0001.jpeg"))
    #shutil.move("C:/Users/Vukasin/Desktop/chest_xray_data_set/chest_xray_data_set/IM-0689-0001.jpeg", "C:/Users/Vukasin/Desktop/chest_xray_data_set/VIRUS/IM-0689-0001.jpeg")
    start_path = "C:/Users/Vukasin/Desktop/chest_xray_data_set/chest_xray_data_set/"
    normal_path = "C:/Users/Vukasin/Desktop/chest_xray_data_set/NORMAL/"
    virus_path = "C:/Users/Vukasin/Desktop/chest_xray_data_set/VIRUS/"
    bacteria_path = "C:/Users/Vukasin/Desktop/chest_xray_data_set/BACTERIA/"
    f = open("chest_xray_metadata.csv", "r")
    #Number,Image_Name,Pnemonia/Normal,,bacteria/virus/''
    for x in f:
        tokens = x.split(",")
        pic = tokens[1]
        try:
            if(tokens[2] == "Normal"):
                shutil.move(start_path+pic, normal_path+pic)
                print("Moved to normal")
            elif(tokens[2] == "Pnemonia"):
                print("Pnemonia" + tokens[4])
                if(tokens[4] == "bacteria\n"):
                    print("Bacteria")
                    shutil.move(start_path + pic, bacteria_path + pic)
                elif(tokens[4] == "Virus\n"):
                    print("Virus")
                    shutil.move(start_path + pic, virus_path + pic)
        except:
            print("Source doesn't exist")
if __name__ == '__main__':
    loadData()