# agent: gpt-a; model: gpt-6-astra; family: gpt
# Independent, exactly symplectic Kerr-only Strang tangent/transpose check.
# This is a numerical cross-check, not a new propagation formula or solver edit.
include(joinpath(@__DIR__,"readout_matrixfree.jl"))

function strang_operator(c)
    get(c,"raman",false) && error("Independent check is instantaneous Kerr only")
    p=readout_setup(c);n=p.n;steps=c["steps"];h=c["length_m"]/steps
    cache=PP._mmgnlse_solver_cache(p.pars)
    half=vec(PP._mmgnlse_linear_propagator(p.pars,0.,h/2,cache))
    stage=zeros(ComplexF64,n,steps);rot=similar(stage);a=vec(p.a)
    linear(x,H)=fft(H.*ifft(x))
    for j in 1:steps
        at=linear(a,half);stage[:,j].=at
        rot[:,j].=exp.(1im*p.gamma*h.*abs2.(at))
        a=linear(at.*rot[:,j],half)
    end
    aw=fftshift(ifft(a));nbar=p.weight.*abs2.(aw);phase=exp.(1im.*angle.(aw))
    function tangent(x;transpose=false)
        q=fft(ifftshift(phase.*complex.(x[1:n],x[n+1:2n])))./sqrt(n)
        if transpose
            for j in steps:-1:1
                q=linear(q,conj.(half));q.*=conj.(@view rot[:,j])
                at=@view stage[:,j]
                q.+=2p.gamma*h.*at.*imag.(conj.(at).*q)
                q=linear(q,conj.(half))
            end
            return q
        end
        q
    end
    function apply(x)
        q=tangent(x;transpose=true)
        for j in 1:steps
            q=linear(q,half);at=@view stage[:,j]
            q=(q.+2im*p.gamma*h.*at.*real.(conj.(at).*q)).*(@view rot[:,j])
            q=linear(q,half)
        end
        y=conj.(phase).*fftshift(ifft(q)).*sqrt(n)
        vcat(real.(y),imag.(y))
    end
    (;apply,nbar,phase,mean_temporal=a,mean_spectral=aw,p)
end

function strang_checks(out)
    path=joinpath(out,"strang-crosscheck.toml")
    isfile(path) && get(TOML.parsefile(path),"complete",false) && return
    base=TOML.parsefile(joinpath(out,"anom_N1_z0.75_K.toml"))["config"]
    # A fixed bright mask is taken from the Raman pilot only to avoid tuning
    # this independent solver's comparison mask to its own output.
    mask=vec(npzread(joinpath(out,"anom_N1_z0.75_R_mf_base.eigen.npz"))["full_mask"])
    rows=Dict{String,Any}[]
    for steps in (96,384,1536,6144,12288)
        c=deepcopy(base);c["steps"]=steps;started=time();op=strang_operator(c);n=op.p.n
        field=lanczos_lowest(op.apply,2n;count=1,maxiter=140,tol=1e-8,label="strang_field_$(steps)")
        amp=lanczos_lowest(x->op.apply(vcat(x,zeros(n)))[1:n],n;
            count=1,maxiter=140,tol=1e-8,label="strang_amp_$(steps)")
        g=vcat(zeros(n),sqrt.(op.nbar./sum(op.nbar)))
        function projected(x)
            y=op.apply(x-dot(g,x).*g)
            y.-dot(g,y).*g.+2dot(g,x).*g
        end
        passive=lanczos_lowest(projected,2n;count=1,maxiter=140,tol=1e-8,label="strang_passive_$(steps)")
        q=vcat(mask.*sqrt.(op.nbar)./sqrt(dot(mask,op.nbar)),zeros(n))
        rng=MersenneTwister(20261010);x=randn(rng,2n);x./=norm(x)
        y=randn(rng,2n);y./=norm(y)
        J(v)=vcat(v[n+1:2n],-v[1:n])
        defect=norm(op.apply(J(op.apply(x)))-J(x))
        symmetry=abs(dot(x,op.apply(y))-dot(y,op.apply(x)))
        defect<1e-7 && symmetry<1e-9 || error("Independent Strang covariance gate failed")
        row=Dict{String,Any}("steps"=>steps,"lambda_min"=>field.values[1],
            "lambda_gen"=>amp.values[1],"lambda_pass"=>passive.values[1],
            "fixed_bright_filter_F"=>dot(q,op.apply(q)),"random_symplectic_covariance_defect"=>defect,
            "random_symmetry_defect"=>symmetry,
            "field_eigen"=>eigen_record(field),"amplitude_eigen"=>eigen_record(amp),
            "passive_eigen"=>eigen_record(passive),"seconds"=>time()-started)
        push!(rows,row)
        open(path,"w") do io
            TOML.print(io,Dict("agent"=>"gpt-a","model"=>"gpt-6-astra","family"=>"gpt",
                "config"=>base,"method"=>"Independent Strang split-step with analytic Kerr JVP and transpose; symplectic at every step",
                "complete"=>steps==12288,"rows"=>rows))
        end
        @printf("STRANG steps=%d min=%.10g gen=%.10g passive=%.10g bright=%.10g defect=%.3g %.1fs\n",
            steps,field.values[1],amp.values[1],passive.values[1],row["fixed_bright_filter_F"],defect,row["seconds"]);flush(stdout)
        op=nothing;GC.gc()
    end
end

if abspath(PROGRAM_FILE)==@__FILE__
    strang_checks(ARGS[1])
end
