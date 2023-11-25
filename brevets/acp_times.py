"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    if 0 <= control_dist_km <= 200:
      total_time = control_dist_km / 34
      open_time_min =  round((total_time - int(total_time)) * 60)
    if 200 < control_dist_km <= 400:
        dist_remain = control_dist_km - 200
        total_time = (200 / 34) + (dist_remain / 32)
        open_time_min =  round((total_time - int(total_time)) * 60)
    if 400 < control_dist_km <= 600:
        dist_remain = control_dist_km - 400
        total_time = (200 / 34) + (200 / 32) + (dist_remain / 30)
        open_time_min =  round((total_time - int(total_time)) * 60)
    if 600 < control_dist_km <= 1000:
        dist_remain = control_dist_km - 600
        total_time = (200 / 34) + (200 / 32) + (200 / 30) + (dist_remain / 28)
        open_time_min =  round((total_time - int(total_time)) * 60)
    if 1000 < control_dist_km <= 1300:
        dist_remain = control_dist_km - 1000
        total_time = (200 / 34) + (200 / 32) + (200 / 30) + (400 / 28) + (dist_remain / 26)
        open_time_min =  round((total_time - int(total_time)) * 60)
    new_time = brevet_start_time.shift(hours=+int(total_time))
    newer_time = new_time.shift(minutes=+open_time_min)
    return  newer_time


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    # Weird oddity if the brevet is at the starting line.
    if control_dist_km == 0:
        total_time = 1
        close_time_min = 0

    # Final controles:
    if control_dist_km >= brevet_dist_km:
        control_dist_km = brevet_dist_km

    if 0 < control_dist_km <= 600:
        total_time = control_dist_km / 15
        close_time_min =  round((total_time - int(total_time)) * 60)
    if 600 < control_dist_km <= 1000:
        dist_remain = control_dist_km - 600
        total_time = (600 / 15) + (dist_remain / 11.428)
        close_time_min =  round((total_time - int(total_time)) * 60)
    if 1000 < control_dist_km <= 1300:
        dist_remain = control_dist_km - 1000
        total_time = (600 / 15) + (400 / 11.428) + (dist_remain / 13.333)
        close_time_min =  round((total_time - int(total_time)) * 60)

    # A rule that states if the brevet is 200km in length, the closing time
    # is 13H30 by default.
    if control_dist_km == brevet_dist_km == 200:
        total_time = 13
        close_time_min = 30

    # A rule for the first 60km of a brevet:
    if control_dist_km < 60:
        close_time_min = (control_dist_km / 20) + 1
        return brevet_start_time.shift(minutes = close_time_min * 60)
    
    # Weird rule for 400km brevet/controle.
    if control_dist_km == brevet_dist_km == 400:
        total_time = 15
        close_time_min = 0
    

    new_time = brevet_start_time.shift(hours=+int(total_time))
    newer_time = new_time.shift(minutes=+close_time_min)
    return  newer_time
   
   

