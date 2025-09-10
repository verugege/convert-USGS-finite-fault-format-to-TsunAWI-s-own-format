#!/usr/bin/env python3
import sys
import re

def parse_param_file(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    # --- Cari header line yg ada nx, ny, Dx, Dy
    header_line = None
    for line in lines:
        if "nx(Along-strike)" in line and "ny(downdip)" in line:
            header_line = line.strip()
            break

    if not header_line:
        raise ValueError("Header line with nx/ny not found!")

    # Regex fleksibel
    nx_match = re.search(r"nx\(Along-strike\)\s*=\s*(\d+)", header_line)
    ny_match = re.search(r"ny\(downdip\)\s*=\s*(\d+)", header_line)
    Dx_match = re.search(r"Dx\s*=\s*([\d.]+)", header_line)
    Dy_match = re.search(r"Dy\s*=\s*([\d.]+)", header_line)

    nx = int(nx_match.group(1)) if nx_match else 0
    ny = int(ny_match.group(1)) if ny_match else 0
    Dx_km = float(Dx_match.group(1)) if Dx_match else 0.0
    Dy_km = float(Dy_match.group(1)) if Dy_match else 0.0

    # --- Cari baris data subfaults (setelah "#Lat. Lon. depth slip ...")
    start_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("#Lat."):
            start_idx = i + 1
            break

    if start_idx is None:
        raise ValueError("Could not find '#Lat. Lon. depth ...' header in file!")

    data_lines = lines[start_idx:]

    subfaults = []
    for line in data_lines:
        if line.startswith("#") or not line.strip():
            continue
        vals = line.split()
        if len(vals) < 11:  # skip kalau bukan data lengkap
            continue

        lat = float(vals[0])
        lon = float(vals[1])
        depth_top_m = float(vals[2]) * 1000.0   # km → m
        slip_m = float(vals[3])
        rake = float(vals[4])
        strike = float(vals[5])
        dip = float(vals[6])
        t_rup = float(vals[7])
        # t_ris, t_fal, mo tidak dipakai di okada_parameter_file

        subfaults.append({
            "lat": lat,
            "lon": lon,
            "depth_top_m": depth_top_m,
            "slip_m": slip_m,
            "strike": strike,
            "dip": dip,
            "rake": rake,
            "t_rup": t_rup,
            "length_m": Dx_km * 1000.0,
            "width_m": Dy_km * 1000.0
        })

    return subfaults

def write_okada_parameter(subfaults, outfile="okada_parameter_file"):
    with open(outfile, "w") as f:
        f.write("# Lon Lat Slip[m] Length[m] Width[m] Strike[deg] Dip[deg] Depth[m] Rake[deg]\n")
        for sf in subfaults:
            f.write(f"{sf['lon']:10.4f} {sf['lat']:9.4f} {sf['slip_m']:8.3f} "
                    f"{sf['length_m']:9.1f} {sf['width_m']:9.1f} "
                    f"{sf['strike']:8.2f} {sf['dip']:8.2f} {sf['depth_top_m']:9.1f} {sf['rake']:8.2f}\n")
    print(f"[INFO] Okada parameter file written: {outfile}")

def write_okada_fault_list(subfaults, outfile="okada_fault_list_file"):
    N = len(subfaults)
    ids = [str(i+1) for i in range(N)]
    times = [f"{sf['t_rup']:.1f}" for sf in subfaults]

    with open(outfile, "w") as f:
        f.write(f"{N}\n")
        f.write(" ".join(ids) + "\n")
        f.write(" ".join(times) + "\n")
    print(f"[INFO] Okada fault list file written: {outfile}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_param2okada.py <param_file>")
        sys.exit(1)

    infile = sys.argv[1]
    subfaults = parse_param_file(infile)
    write_okada_parameter(subfaults, "okada_parameter_file")
    write_okada_fault_list(subfaults, "okada_fault_list_file")
