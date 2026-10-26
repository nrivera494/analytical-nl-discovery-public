# agent: gpt-a; model: gpt-6-astra; family: gpt
# T-20261008-gpt-a-01. Deterministic finite-volume entropy continuation of
# dispersionless gain Euler. This is not a proof of shock time or smoothness.
include("similariton_gain.jl")
minmod3(a,b,c) = (sign(a)==sign(b)==sign(c)) ? sign(a)*min(abs(a),abs(b),abs(c)) : 0.
function flux_rhs(r,m,k,dx)
    n=length(r); u=m./max.(r,1e-30)
    sr=zeros(n);su=zeros(n)
    @inbounds for j=2:n-1
        sr[j]=minmod3(2(r[j]-r[j-1]),(r[j+1]-r[j-1])/2,2(r[j+1]-r[j]))
        su[j]=minmod3(2(u[j]-u[j-1]),(u[j+1]-u[j-1])/2,2(u[j+1]-u[j]))
    end
    fr=zeros(n+1);fm=zeros(n+1)
    @inbounds for j=1:n+1
        jl=max(1,j-1);jr=min(n,j)
        rl=max(r[jl]+sr[jl]/2,1e-30); rr=max(r[jr]-sr[jr]/2,1e-30)
        ul=u[jl]+su[jl]/2;ur=u[jr]-su[jr]/2
        ml=rl*ul;mr=rr*ur
        a=max(abs(ul)+sqrt(k*rl),abs(ur)+sqrt(k*rr))
        fr[j]=(ml+mr-a*(rr-rl))/2
        fm[j]=(ml*ul+mr*ur+k*(rl*rl+rr*rr)/2-a*(mr-ml))/2
    end
    return -diff(fr)./dx,-diff(fm)./dx
end
function hydro_measure(r,m,x,z,k)
    dx=x[2]-x[1];u=m./max.(r,1e-30);c=sqrt.(k.*r)
    good=(r[2:end-1].>.02maximum(r))
    ux=(u[3:end].-u[1:end-2])./(2dx)
    cx=(c[3:end].-c[1:end-2])./(2dx)
    rx=(r[3:end].-r[1:end-2])./(2dx).*exp(-z/3)
    Dict("gain_length"=>z,"mass"=>sum(r)*dx,
        "compressive_velocity_gradient"=>maximum(max.(-ux[good],0.)),
        "compressive_riemann_gradient"=>maximum(max.(-ux[good].+2abs.(cx[good]),0.)),
        "maximum_scaled_density_gradient"=>maximum(abs.(rx[good])),
        "minimum_density"=>minimum(r),
        "time_guard_fraction"=>sum(r[abs.(x).>.85maximum(abs,x)])/sum(r))
end
function hydro_case(c,defaults,raw)
    getc(key,fallback)=get(c,key,get(defaults,key,fallback))
    n=Int(getc("nt",2048));window=Float64(getc("window",32.));dx=window/n
    x=collect(range(-window/2+dx/2,step=dx,length=n))
    shape=getc("shape","gaussian");width=Float64(getc("width",1.));chirp=Float64(getc("chirp",0.))
    k=Float64(getc("k",1/18));len=Float64(getc("length",4.));interval=Float64(getc("save_interval",.02))
    cfl=Float64(getc("cfl",.3))
    if shape=="shock_example"
        ell=Float64(getc("ell",.025)); cp=1 .-tanh.(x./ell)./8
        v=-tanh.(x./ell)./4
        taper=max.(0.,1 .-max.(abs.(x).-1,0.).^2)
        r=cp.^2 ./ k .* taper;m=r.*v
    elseif shape=="parabola_exact"
        r=max.(1 .-(x./width).^2,0.);r.*=(4/3)/(sum(r)*dx)
        m=r.*(chirp.*x)
    else
        ini=initial_pulse(x,shape,width,0.,1.;order=4)
        r=abs2.(ini.field);m=r.*(chirp.*x)
    end
    rows=[hydro_measure(r,m,x,0.,k)];snapr=[copy(r)];snapm=[copy(m)];snapz=[0.]
    z=0.;steps=0;minrho=minimum(r);startmass=sum(r)*dx
    elapsed=@elapsed begin
      for target in interval:interval:len
        while z<target-1e-12
            vel=m./max.(r,1e-30)
            h=min(cfl*dx/maximum(abs.(vel).+sqrt.(k.*r)),target-z)
            fac=exp(h/2);r .*=fac;m .*=fac
            dr,dm=flux_rhs(r,m,k,dx);r1=r.+h.*dr;m1=m.+h.*dm
            if minimum(r1)<-1e-12;error("lost positivity");end
            r1=max.(r1,1e-30);m1[r1.<1e-18].=0.
            dr,dm=flux_rhs(r1,m1,k,dx)
            r=(r.+r1.+h.*dr)./2;m=(m.+m1.+h.*dm)./2
            minrho=min(minrho,minimum(r));r=max.(r,1e-30);m[r.<1e-18].=0.
            r .*=fac;m .*=fac;z+=h;steps+=1
        end
        push!(rows,hydro_measure(r,m,x,z,k))
        if abs(target*2-round(target*2))<1e-8 || target≈len
            push!(snapr,copy(r));push!(snapm,copy(m));push!(snapz,z)
        end
      end
    end
    label=c["label"];mkpath(raw)
    out=Dict("agent"=>"gpt-a","model"=>"gpt-6-astra","family"=>"gpt",
       "label"=>label,"shape"=>shape,"width"=>width,"chirp"=>chirp,"nt"=>n,"window"=>window,
       "k"=>k,"length"=>len,"cfl"=>cfl,"steps"=>steps,"elapsed_seconds"=>elapsed,"minimum_raw_density"=>minrho,
       "mass_gain_relative_error"=>sum(r)*dx/(startmass*exp(len))-1,"rows"=>rows,
       "method"=>"MUSCL MC/Rusanov flux, SSP-RK2 homogeneous step, exact Strang gain source")
    open(joinpath(raw,label*".toml"),"w") do io;TOML.print(io,out);end
    npzwrite(joinpath(raw,label*".npz"),Dict("x"=>x,"z"=>snapz,"density"=>hcat(snapr...),"momentum"=>hcat(snapm...)))
    @printf("%s hydro: %.2fs steps=%d gradient=%.4g mass=%.2g\n",label,elapsed,steps,last(rows)["compressive_riemann_gradient"],out["mass_gain_relative_error"]);flush(stdout)
end
function hydro_main()
    cfg=TOML.parsefile(ARGS[1]);defaults=get(cfg,"defaults",Dict{String,Any}())
    for c in cfg["cases"];hydro_case(c,defaults,cfg["raw_location"]);end
end
abspath(PROGRAM_FILE)==(@__FILE__) && hydro_main()
