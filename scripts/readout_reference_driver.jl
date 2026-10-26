# agent: gpt-a; model: gpt-6-astra; family: gpt
# Run gates before the reference sweep, in a single Julia process.
include(joinpath(@__DIR__,"readout_covariance.jl"))
include(joinpath(@__DIR__,"readout_notebook_gate.jl"))
config=TOML.parsefile(ARGS[1]);out=config["raw_location"]
include(joinpath(out,"raman_bath_spectrum.jl"))
if get(config,"run_gates",true)
    weak=deepcopy(config["cases"][1]);weak["label"]="gate_weak_power";weak["peak_power_W"]=1e-6
    weak["nt"]=128;weak["steps"]=32;weak["raman"]=false
    covariance_case(weak,out)
    gate=TOML.parsefile(joinpath(out,"gate_weak_power.toml"))
    abs(gate["direct_filter_F"]-1)<1e-7 || error("Weak-power gate failed")
    anchor=TOML.parsefile(joinpath(out,"pilot_kerr_phi1.toml"))
    abs(anchor["lambda_min"]-(sqrt(2)-1)^2)<1e-6 || error("Kerr anchor gate failed")
    notebook_gate(out)
end
for c in config["cases"]
    covariance_case(c,out)
end
