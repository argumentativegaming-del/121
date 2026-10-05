import sys, json, lupa
from lupa import LuaRuntime
L = LuaRuntime(unpack_returned_tuples=True)
def conv(o):
    if lupa.lua_type(o)=='table':
        keys=list(o.keys())
        if keys and all(isinstance(k,int) for k in keys) and sorted(keys)==list(range(1,len(keys)+1)):
            return [conv(o[k]) for k in sorted(keys)]
        return {str(k):conv(v) for k,v in o.items()}
    return o
src=open(sys.argv[1]).read()
t=L.execute(src)
json.dump(conv(t),open(sys.argv[2],'w'),indent=1)
