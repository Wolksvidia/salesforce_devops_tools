from build_manifest import build_manifest
from diff_maker import diff_maker

if __name__ == "__main__":
    diff_maker.build_diff_files('src','CCC')
    build_manifest.custom_package_xml_generator('CCC')