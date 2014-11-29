__author__ = 'Akhil'

import numpy as np
import pandas as pd
import networkx as nx
import datetime as dt
import matplotlib.pyplot as plt

DG = nx.DiGraph()

def createGraph(row):

    # Add nodes for the sender and receiver if they don't already exist
    if not DG.has_node(row.SenderEmail):
        DG.add_node(row.SenderEmail,{"EID":row.SenderEID})

    if not DG.has_node(row.ReceiverEmail):
        DG.add_node(row.ReceiverEmail,{"EID":row.ReceiverEID})

    # Add edge if it doesn't exist
    if not DG.has_edge(row.SenderEmail,row.ReceiverEmail):
        DG.add_edge(row.SenderEmail,row.ReceiverEmail,{"MID":row.mid,"SentDate":row.SentDate,"Type":row.ReceiverType})

    return None

if __name__ == "__main__":

    # get the datafile
    data = pd.read_csv("enronDataCleaned.csv")
    data["SentDate"] = data.SentDate.apply(lambda x: dt.datetime.strptime(x,"%Y-%m-%d %H:%M:%S"))
    data["Year"] = data.SentDate.apply(lambda x: x.year)
    data["Month"] = data.SentDate.apply(lambda x: x.month)
    data["Day"] = data.SentDate.apply(lambda x: x.day)

    #subset and create graph
    data2 = data[(data["Year"] == 2000) & (data["Month"] == 10)]
    data2.apply(createGraph,1)
    nx.draw_networkx(DG)
    plt.show()

    # get the adj matrix
    nodes = DG.nodes()
    nodes.sort()
    mat2000 = nx.to_numpy_matrix(DG,nodes)
    eigCentrality = nx.eigenvector_centrality_numpy(DG)
    #
    # plt.bar(np.arange(len(eigCentrality)),eigCentrality.values(),)
    # plt.show()

    # nx.draw(DG)
    # plt.title("Oct 2000")
    # plt.show()
