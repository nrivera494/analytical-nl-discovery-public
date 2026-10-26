# Minimal JSON writer (no package dependency), same as the one inlined in contract.jl.
function json(io, x::AbstractDict, ind="")
    println(io, "{"); ks = collect(keys(x))
    for (i, k) in enumerate(ks)
        print(io, ind, "  \"", k, "\": "); json(io, x[k], ind * "  "); println(io, i < length(ks) ? "," : "")
    end
    print(io, ind, "}")
end
json(io, x::AbstractVector, ind="") = (print(io, "["); for (i, v) in enumerate(x); json(io, v, ind); i < length(x) && print(io, ", "); end; print(io, "]"))
json(io, x::AbstractMatrix, ind="") = json(io, [x[i, :] for i in 1:size(x, 1)], ind)
json(io, x::Real, ind="") = print(io, isfinite(x) ? repr(Float64(x)) : "null")
json(io, x::AbstractString, ind="") = print(io, "\"", x, "\"")
json(io, x::Bool, ind="") = print(io, x ? "true" : "false")
