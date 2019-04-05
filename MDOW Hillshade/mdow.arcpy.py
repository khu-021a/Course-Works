import math as m
import arcpy as _


def hillshade_mdow(in_raster, out_raster, azimuth, altitude, model_shadows, z_factor):
    """MDOW hillshade. Here is a new model of MDOW hillshade with a little modification."""
    try:
        deg2rad = 180 / m.pi
        azimuth_tuple = (225, 270, 315, 360)

        _.AddMessage("Generating slope and aspect rasters...")
        slope_init = _.sa.Slope(in_raster, "DEGREE", z_factor)
        _.AddMessage("Slope raster has been generated successfully!")
        aspect_init = _.sa.Aspect(in_raster)
        _.AddMessage("Aspect raster has been generated successfully!")

        _.AddMessage("Generating hillshades...")
        hillshade_init = _.sa.Hillshade(in_raster, azimuth, altitude, model_shadows, z_factor)
        hillshade_dict = {x: _.sa.Hillshade(in_raster, x, altitude, model_shadows, z_factor) for x in azimuth_tuple}
        _.AddMessage("Hillshades with initial direction and 4 other directions have been generated successfully!")

        _.AddMessage("Calculating the weights of hillshades with 4 special directions...")
        weight_dict = {y: (_.sa.Cos((aspect_init - y) / deg2rad) + 1) for y in azimuth_tuple}
        total = 0
        for v in weight_dict.values():
            total += v
        weight_dict = {k: (w / _.sa.SquareRoot(total * 2)) for (k, w) in weight_dict.items()}
        _.AddMessage("Weight calculations have finished successfully!")

        _.AddMessage("Generating MDOW hillshade...")
        hillshade_md = 0
        for k in hillshade_dict.keys():
            hillshade_md += (hillshade_dict[k] * weight_dict[k])
        _.AddMessage("MDOW hillshade has been generated successfully!")

        _.AddMessage("Merging with initial hillshade...")
        weight_merge = _.sa.Square(_.sa.Sin(_.sa.Cos(altitude / deg2rad) * _.sa.Sin(slope_init / deg2rad) *
                                            _.sa.Cos((aspect_init - azimuth) / deg2rad) +
                                            _.sa.Sin(altitude / deg2rad) * _.sa.Cos(slope_init / deg2rad)))
        hillshade_final = weight_merge * hillshade_md + (1 - weight_merge) * hillshade_init
        _.AddMessage("With slight smooth...")
        hillshade_final = _.sa.FocalStatistics(hillshade_final, _.sa.NbrRectangle(5, 5, "CELL"), "MEAN")
        _.AddMessage("Final hillshade has finished successfully!")
        _.AddMessage("Saving final MDOW hillshade...")
        hillshade_final.save(out_raster)
        _.AddMessage("Final MDOW hillshade has been saved successfully!")
    except Exception as e:
        _.AddError("Exceptions arise! Fail to execute the operations of MDOW hillshade!")
        _.AddError("Message: {0}".format(e.message))
    finally:
        _.AddMessage("Execution of MDOW hillshade ends!")

in_raster = _.GetParameterAsText(0)
out_raster = _.GetParameterAsText(1)
azm = float(_.GetParameterAsText(2))
alt = float(_.GetParameterAsText(3))
shadows = _.GetParameterAsText(4)
z_f = _.GetParameterAsText(5)

hillshade_mdow(in_raster, out_raster, azm, alt, shadows, z_f)