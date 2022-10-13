import itertools as itertools
import pandas as pd
import os

if not os.path.exists("solutions.json"):
    print("remote loading")
    df = pd.read_json(
        "https://zenodo.org/record/5526707/files/solutions.json?download=1"
    )
    df.to_json("solutions.json", orient="records")
else:
    print("local loading")
    df = pd.read_json("solutions.json")

print(df.shape)
print(df.columns)
df=df[:10000]

def get_hidden_sector(l):

    com = list(itertools.combinations_with_replacement(l, 2))
    suma = set([abs(sum(i)) for i in com])

    final = []

    for s in suma:
        cond = [i for i in com if abs(sum(i)) == s]
        aplanar = [item for sublist in cond for item in sublist]
        resta = set(l).difference(set(aplanar))

        if not resta:
            l_ = l.copy()
            cond_ = cond
            N = len(l)

            combs = []

            equal = [par for par in cond_ if par[0] == par[1]]
            ind_eq = [cond.index(eq) for eq in equal]
            
            for ind in ind_eq:
                cond_.pop(ind)

            for par in cond_:
                try:
                    for val in par:
                        l_[l_.index(val)] = 0
                    N = N - 2
                    combs.append(par)
                except:
                    pass
                    # print("Discharge pair", par)
            
            for par in equal:
                ind = []
                for val in par:
                    try:
                        ind.append(l_.index(val))
                    except:
                        pass
                for ind_ in ind:
                    l_[ind_] = 0

                if len(set(ind)) == 1:
                    N = N - 1
                elif len(set(ind)) != 1:
                    N = N - len(set(ind))

                combs.append(par)

            if N == 0:
                final.append({"S": s, "ψ": combs})

            del l_, cond_

    return final

assert get_hidden_sector([1,2,-3,4,5])[0].get('S')==6
assert get_hidden_sector([1,2,-3,-3,4,5])[0].get('S')==6
assert get_hidden_sector([1,1,2,-3,-3,4,5,5])[0].get('S')==6
#aψ1ψ1+bψ1ψ2+cψ1,ψ3 → https://www.wolframalpha.com/input?i=Rank%20{{a,b,c},{b,0,0},{c,0,0}}
assert get_hidden_sector([1,2,-3,4,5,9,9])==[]
get_hidden_sector([1,1,2,-3,4,5])
#aψ1ψ2+bψ1ψ3 → https://www.wolframalpha.com/input?i=rank+{{0,a,b},{a,0,0},{b,0,0}}
assert get_hidden_sector([1,1,2,-3,4,5])==[]
assert get_hidden_sector([1,1,2,-3,-3,4,5])==[]
assert get_hidden_sector([1,2,-3,4,5,8])==[]
assert get_hidden_sector([1,2,-3,4,5,8,8])==[]
assert get_hidden_sector([])==[]
assert get_hidden_sector([1, 1, 1, 1, 1, -2, -2, -2, -2, 3])==[]
assert get_hidden_sector([1, 2, 2, 2, -3, -5, -6, 7])[0].get('S')==4
assert get_hidden_sector( [1, 2, 2, 4, -5, -5, -7, 8] )[0].get('S')==3
# Ana test
assert get_hidden_sector([2, -3, -4, 5, -6, 7, 7, -8])[0].get('S')==1
assert get_hidden_sector([3, 5, -8, 9, -10, -14, 15])==[] # Dirac triplet [-10,5,15] (s=5)
assert get_hidden_sector([3, 5, -8, 9, -10, -14, 15, 20,-30, 35])==[] 

df["hidden"] = df["solution"].apply(get_hidden_sector)

print("*" * 20)
#print(df.iloc[0].to_dict())
df2=df[df['hidden'].apply(len)>0].reset_index(drop=True)
print(df2)
print(df2.shape)
df2.to_json('ana.json',orient='records')
