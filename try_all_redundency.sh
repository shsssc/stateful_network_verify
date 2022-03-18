for r in {2..16}; do
    echo "Redundency: $r"
    python3 generateFatTree.py -d fatTree$r -r $r
    python3 generateNetworkCode.py -d fatTree$r -s EcmpTorP1T1
    cd fatTree$r
    make
    time make klee
    cd ..
done