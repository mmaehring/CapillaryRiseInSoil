using Plots
using Statistics
using Unitful
using UnitfulRecipes
using LsqFit
using Measurements

@. model(x, p) = p[1]*sqrt(x) + p[2];

function calculate_pore_size(factor)
        γ = 72e-3u"N/m" # newtons per meter
        η = 8.9e-4u"Pa*s" # Pa * s
        ϕ = 50u"°" # degree
        ϕ_rad = ϕ|>u"rad"
        r = 2 * factor^2 * η / (γ * cos(ϕ_rad))
        r_μm = r |> u"μm"
end;

function get_data(nr)
        if nr == 2
                timearray = [ 0.,  3.,  5.,  7., 10., 12., 14., 17., 19., 21., 24., 26., 29.,
                               31., 33., 36., 38., 40., 43., 45., 47., 50., 52., 55., 57., 59.,
                               62., 64., 66., 73.] * u"s";
                MH = [1.06459068, 1.02910433, 1.10007704, 1.24202246, 1.40171106, 1.49042695, 1.84529051, 2.07595183, 2.1824109 , 2.27112679,
                      2.35984268, 2.43081539, 2.5017881 , 2.55501763, 2.71470624, 2.89213802, 2.98085391, 3.14054251, 3.21151522, 3.24700158,
                      3.28248793, 3.35346065, 3.40669018, 3.42443336, 3.44217654, 3.47766289, 3.49540607, 3.51314925, 3.53089243, 3.58412196]* u"cm";

                σMH =  [0.07604219, 0.07350745, 0.07857693, 0.08871589, 0.10012222, 0.10645907, 0.13180647, 0.14828227, 0.15588649, 0.16222334,
                        0.16856019, 0.17362967, 0.17869915, 0.18250126, 0.19390759, 0.20658129, 0.21291814, 0.22432446, 0.22939394, 0.23192868,
                        0.23446342, 0.2395329 , 0.24333501, 0.24460238, 0.24586975, 0.24840449, 0.24967186, 0.25093923, 0.2522066 , 0.25600871]* u"cm";

                AH = [0.98474638, 0.98918217, 1.07641947, 1.16750111, 1.30654311, 1.45937639, 1.66490154, 1.84529051, 2.13805295, 2.23564043,
                      2.32435632, 2.40420062, 2.47517333, 2.53727446, 2.63105983, 2.79159334, 2.65556231, 3.0695698 , 3.18490045, 3.23812999,
                      3.27065915, 3.32684588, 3.388947  , 3.42443336, 3.44217654, 3.4687913 , 3.49540607, 3.51314925, 3.53089243, 3.58412196]* u"cm";

                σAH = [0.05516578, 0.04666377, 0.02710315, 0.04923532, 0.07020235, 0.03030225, 0.14841794, 0.16463455, 0.03319445, 0.02805443,
                       0.02805443, 0.02290634, 0.02290634, 0.01774318, 0.04773573, 0.06864958, 0.71031831, 0.04859169, 0.02290634, 0.01254632,
                       0.01024403, 0.02290634, 0.01774318, 0.03709187, 0.03709187, 0.03709187, 0.03709187, 0.03709187, 0.03709187, 0.03709187]* u"cm";

        elseif nr == 3
                timearray = [ 0.,  2.,  5.,  7., 10., 12., 14., 17., 19., 21., 24., 26., 28., 33.] * u"s"
                MH =  [1.41945424, 2.98085391, 3.74381056, 4.80840124, 5.26972387, 5.74878968,
                      5.94396464, 6.65369176, 6.76015082, 6.83112354,6.86660989, 6.91983943, 6.9375826 , 6.95532578] * u"cm";
                σMH = [0.10138959, 0.21291814, 0.26741504, 0.34345723, 0.37640885, 0.41062783, 0.4245689,
                        0.4752637 , 0.48286792, 0.4879374 ,0.49047214, 0.49427424, 0.49554161, 0.49680898] * u"cm";
                AH =  [1.21540769, 2.20902566, 3.37120382, 4.28497749, 5.04793415, 5.51812836, 5.85524875,
                       6.30769979, 6.71579288, 6.80450877, 6.8577383 , 6.90209625, 6.9375826 , 6.95532578] * u"cm";
                σAH = [0.12546321, 0.45329103, 0.2227929 , 0.30987128, 0.13570922, 0.14083211, 0.05884746, 0.20742577, 0.26555557, 0.18325075,
                               0.10037057, 0.14194542, 0.27050648, 0.27050648] * u"cm";
        elseif nr==4
                timearray = [ 0.,  3.,  5.,  7., 10., 12., 15., 17., 19.] * u"s"
                MH = [1.98723594, 3.17602887, 4.15190366, 4.80840124, 5.28746705, 5.69556014, 6.24559866, 6.51174633, 6.52948951] * u"cm";
                σMH = [0.14194542, 0.2268592 , 0.29656455, 0.34345723, 0.37767622, 0.40682572, 0.44611419, 0.46512474, 0.46639211] * u"cm";
                AH = [1.51704172, 2.59050399, 3.67283785, 4.48902404, 5.05680573, 5.50038519, 5.97945099, 6.38754409, 6.52948951] * u"cm";
                σAH = [0.27913803, 0.34572648, 0.28426026, 0.19205846, 0.14083211, 0.12034009, 0.16132312, 0.0793499 , 0.09301278] * u"cm";
        end
        return (timearray, MH, σMH, AH, σAH)
end

function χ_sqr_det(fit, time, height, error)
        new_mod_func(time) = fit.param[1] * sqrt.(time)*u"cm/s^(1/2)" .+ fit.param[2]*u"cm"
        χ² = sum((new_mod_func.(time) .- height).^2 ./ error.^2)
        χ²_fit_calc = sum((fit.resid*u"cm").^2 ./ error.^2)
        dof = length(ustrip.(height)) - 2
        χ²dof = χ²/dof
        return dof, χ², χ²dof #, χ²_fit_calc, χ²_fit_calc/dof
end

timearray, MH, σMH, AH, σAH = get_data(4);

p0 = [0.5, 0.05];

# Maximum fit
Mfit = curve_fit(model, ustrip.(timearray), ustrip.(MH), (1 ./ ustrip.(σMH)).^2, ustrip.(p0))
MsqrtC = Mfit.param[1]
MsigmaC = stderror(Mfit)[1]
Mcoinfidence = confidence_interval(Mfit, 0.05)[1]
MC = (MsqrtC ± MsigmaC)u"cm/s^(1/2)"
Mr = calculate_pore_size(MC)

# Average fit
Afit = curve_fit(model, ustrip.(timearray), ustrip.(AH), (1 ./ ustrip.(σAH)).^2 , ustrip.(p0));
AsqrtC = Afit.param[1]
AsigmaC = stderror(Afit)[1]
Acoinfidence = confidence_interval(Afit, 0.05)[1]
AC = (AsqrtC ± AsigmaC)u"cm/s^(1/2)"
Ar = calculate_pore_size(AC)

## Plotting M
linspace = timearray[1]:0.01u"s":timearray[end]

new_model_M(x) =  MsqrtC * u"cm/s^(1/2)"* sqrt(x) + Mfit.param[2]*u"cm"
scatter(timearray, MH .± σMH, label="Maxima for every column",
        title="Water level, sand 3",
        xticks=xticks = (0:5:(maximum(ustrip.(linspace)) - maximum(ustrip.(linspace))%10)),
        xlabel="Time",
        ylabel="Penetrated depth",
        titlefont=12
)
plot!(linspace, new_model_M.(linspace),
        label="Fitted to max value for every column, L(t)=$(round(Mfit.param[1]; digits=2))√t + $(round(Mfit.param[2]; digits=2))",
        legend=:bottomright)

# savefig("maximum")
# quality of plot:
χ_sqr_det(Mfit, timearray, MH, σMH)

## Plotting A

new_model_A(x) =  AsqrtC * u"cm/s^(1/2)"* sqrt(x) + Afit.param[2]*u"cm"

linspace = timearray[1]:0.01u"s":timearray[end]
plot(linspace, new_model_A.(linspace), label="Fitted to averages", legend=:bottomright)
scatter!(timearray, AH .± σAH,
        xlabel = "Time",
        ylabel = "Penetrated depth",
        label="Mean for every column", title="Means",
        xticks = (0:10:(maximum(ustrip.(linspace)) - maximum(ustrip.(linspace))%10))
)

# quality of plot:
χ_sqr_det(Afit, timearray, AH, σAH)
