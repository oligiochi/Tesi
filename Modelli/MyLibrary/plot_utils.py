from pathlib import Path
import matplotlib.pyplot as plt
def plotAndamentoPlot(predictions,Output,input,path:str=None):
    plt.figure(figsize=(10, 6))
    plt.scatter(input, Output, color='blue', label='Dati reali',marker='s')
    color = (224/255, 117/255, 118/255)
    if predictions is not None:
        plt.plot(input, predictions, color=color, label='Predizioni del modello')
        plt.scatter(input, predictions, color=color,marker='x')
    #plt.plot(X_real, y_real, color='green', label='Funzione reale')

    plt.xlabel('Frequenza')
    plt.ylabel('Pressione')
    plt.title('Confronto tra la funzione reale e le predizioni del modello')
    #plt.title('Accuracy: {:.2f}'.format(score))
    plt.legend()
    if path is not None and not Path(path).exists():
        plt.savefig(path)
    plt.show()