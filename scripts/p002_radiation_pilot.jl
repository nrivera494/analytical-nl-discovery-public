# agent: gpt-a; model: gpt-6-astra; family: gpt
# Exploratory full nonlinear run; not evidence for an infinite-distance theorem.
include(joinpath(@__DIR__,"p002_nextorder_full.jl"))
mode=length(ARGS)>1 ? ARGS[2] : "base"
if mode=="base"
    next_full(ARGS[1],"delta085_r0006",next_parameters(.85);r=.006,nt=16384,window=2048.,
        dz=.02,zs=[0.,50.,100.,150.,200.,250.,300.,350.,400.])
elseif mode=="convergence"
    next_full(ARGS[1],"doublewindow",next_parameters(.85);r=.006,nt=32768,window=4096.,
        dz=.02,zs=[0.,50.,100.,150.,200.,250.,300.,350.,400.])
    next_full(ARGS[1],"halfstep",next_parameters(.85);r=.006,nt=16384,window=2048.,
        dz=.01,zs=[0.,50.,100.,150.,200.,250.,300.,350.,400.])
else
    error("Unknown mode $mode")
end
