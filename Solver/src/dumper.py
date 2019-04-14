import os
import struct
import config


def arch2mode(arch):
    return arch.replace("_", "").upper()


def dump(newcode, arch):
    version = int(arch.split("_")[1])
    if version < 40:
        tmp_bin = "/tmp/tmp_dumper.bin"
        fout = open(tmp_bin, "wb")
        fout.write(struct.pack("<Q", int(newcode, 16)))
        fout.close()
        cmd = "{0} -b {1} {2} 2>&1".format(config.nvdisasm_path, arch2mode(arch), tmp_bin)
        tmp_read = os.popen(cmd).read()
        rmfile = "rm {0}".format(tmp_bin)
        os.system(rmfile)
        return tmp_read
    else:
        # create a tmp cubin file in working directory
        tmp_cubin = "%s/data/%s/%s.tmp.cubin" % (config.work_dir, arch, arch)
        f = open(tmp_cubin, 'rb+')
        # @todo 为什么是这个数？
        f.seek(904)
        f.write(struct.pack('Q', int(newcode, 16)))
        f.close()
        cmd = "%s -arch %s -sass %s 2>&1" % (config.cuobjdump_path, arch, tmp_cubin)
        tmp_read = os.popen(cmd).read()
        return tmp_read
