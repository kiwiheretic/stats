import types

def permute_values(permute_indexes, values):
    vdict = {} 
    for idx, regidx in enumerate(permute_indexes):
        if type(regidx) == types.ListType:
            for ii in regidx:
                v = values[idx]
                vdict[ii] = v
        else:
            v = values[idx]
            vdict[regidx] = v
    vlist = []
    for ii in range(1,18):
        if ii in vdict.keys():
            vlist.append(vdict[ii])
        else:
            vlist.append(None)
    return vlist
