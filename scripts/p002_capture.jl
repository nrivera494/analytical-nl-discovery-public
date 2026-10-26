# agent: gpt-a; model: gpt-6-astra; family: gpt
include(joinpath(@__DIR__,"p002_common.jl"))
out=ARGS[1];mode=length(ARGS)>1 ? ARGS[2] : "main";mkpath(out)
isfile(joinpath(@__DIR__,"..","runs","2026-10-04-gpt-a-material","prediction_manifest.json")) || error("Missing frozen manifest")
deltas=[0.,.5,1.,1.5,2.,3.,MAT["delta_physical"]]
if mode=="main"
    run_capture(out,"scalar_control";r=0.,nm=1)
    for (j,d) in enumerate(deltas),r in (.003,.01,.03,.1)
        run_capture(out,"d$(j)_r$(r)";r,delta=d)
    end
elseif mode=="small"
    for (j,d) in enumerate(deltas),r in (.0001,.0003,.001)
        run_capture(out,"d$(j)_r$(r)";r,delta=d)
    end
elseif mode=="convergence"
    for (j,r,d) in ((1,.01,1.),(2,.1,3.),(3,.01,MAT["delta_physical"]))
        run_capture(out,"case$(j)_halfstep";r,delta=d,dz=.005)
        run_capture(out,"case$(j)_doublewindow";r,delta=d,nt=8192,window=640.)
        run_capture(out,"case$(j)_doubleresolution";r,delta=d,nt=8192)
        run_capture(out,"case$(j)_long";r,delta=d,zeta=40.,savezetas=[0.,10.,20.,30.,40.],window=640.,nt=8192)
        run_capture(out,"case$(j)_three_modes";r,delta=d,nm=3)
    end
    for r in (.0001,.003,.01,.03,.1)
        run_capture(out,"physical_r$(r)";r,delta=MAT["delta_physical"],physical=true,nm=3,dz=.0025)
    end
elseif mode=="three_scaling"
    for r in (.0001,.0003,.001,.003,.03,.1),d in (0.,1.)
        run_capture(out,"three_r$(r)_d$(d)";r,delta=d,nm=3)
    end
else
    error("Unknown mode $mode")
end
