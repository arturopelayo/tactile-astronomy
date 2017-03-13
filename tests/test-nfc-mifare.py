#
# libnfc  1.7.1
#
#     Main Page
#     Modules
#     Data Structures
#     Files
#     Directories
#
#     libnfc reference manual
#
# Examples
# Introduction
#
# This page presents some examples to help developers which use libnfc.
# Simple tag UID reader.
#
# This short commented code example should be helpful to quick start development with libnfc, it grab the first available NFC device and print the first found ISO14443-A tag (e.g. MIFARE Classic, MIFARE Ultralight).
#
# // To compile this simple example:
# // $ gcc -o quick_start_example1 quick_start_example1.c -lnfc
#
# #include <stdlib.h>
# #include <nfc/nfc.h>
#
# static void
# print_hex(const uint8_t *pbtData, const size_t szBytes)
# {
#   size_t  szPos;
#
#   for (szPos = 0; szPos < szBytes; szPos++) {
#     printf("%02x  ", pbtData[szPos]);
#   }
#   printf("\n");
# }
#
def print_hex(string):
    """Dumps data as hexstrings"""
    bits = []
    if type(string) is int:
        return '%02x' % string
    for x in string:
        if type(x) is str:
            x = ord(x)
        bits += ['%02x' % x]
    return ' '.join(bits)


from nfc import *
import ctypes
# int
# main(int argc, const char *argv[])
# {
def main():

    #   nfc_device *pnd;
    #   nfc_target nt;
    pnd = None
    nt = nfc_target()
    #
    #   // Allocate only a pointer to nfc_context
    #   nfc_context *context;
    #
    #   // Initialize libnfc and set the nfc_context
    #   nfc_init(&context);
    context = ctypes.pointer(nfc_context())
    nfc_init(ctypes.byref(context))

    #   if (context == NULL) {
    #     printf("Unable to init libnfc (malloc)\n");
    #     exit(EXIT_FAILURE);
    #   }
    if context is None:
        print "Unable to init libnfc"
        exit(1)
    #   // Display libnfc version
    #   const char *acLibnfcVersion = nfc_version();
    #   (void)argc;
    #   printf("%s uses libnfc %s\n", argv[0], acLibnfcVersion);
    print "%s uses libnfc %s" % ("this", nfc_version())
    #
    #   // Open, using the first available NFC device which can be in order of selection:
    #   //   - default device specified using environment variable or
    #   //   - first specified device in libnfc.conf (/etc/nfc) or
    #   //   - first specified device in device-configuration directory (/etc/nfc/devices.d) or
    #   //   - first auto-detected (if feature is not disabled in libnfc.conf) device
    #   pnd = nfc_open(context, NULL);
    ncs = (nfc_connstring * 1)()
    devices_found = nfc_list_devices(context, ncs, 1)
    if devices_found == 0:
        print "No devices found"
        exit(1)
    pnd = nfc_open(context, ncs[0])
    #
    #   if (pnd == NULL) {
    #     printf("ERROR: %s\n", "Unable to open NFC device.");
    #     exit(EXIT_FAILURE);
    #   }
    if pnd is None:
        print "Unable to open NFC device"
        exit(1)
    #   // Set opened NFC device to initiator mode
    #   if (nfc_initiator_init(pnd) < 0) {
    #     nfc_perror(pnd, "nfc_initiator_init");
    #     exit(EXIT_FAILURE);
    #   }
    if nfc_initiator_init(pnd) < 0:
        print "Error occurred setting device to initiator mode"
        exit(1)
    #
    #   printf("NFC reader: %s opened\n", nfc_device_get_name(pnd));
    print "NFC reader: %s opened\n" % nfc_device_get_name(pnd)

    #
    #   // Poll for a ISO14443A (MIFARE) tag
    #   const nfc_modulation nmMifare = {
    #     .nmt = NMT_ISO14443A,
    #     .nbr = NBR_106,
    #   };
    nmMifare = nfc_modulation()
    nmMifare.nmt = NMT_ISO14443A
    nmMifare.nbr = NBR_106

    #   if (nfc_initiator_select_passive_target(pnd, nmMifare, NULL, 0, &nt) > 0) {
    #     printf("The following (NFC) ISO14443A tag was found:\n");
    #     printf("    ATQA (SENS_RES): ");
    #     print_hex(nt.nti.nai.abtAtqa, 2);
    #     printf("       UID (NFCID%c): ", (nt.nti.nai.abtUid[0] == 0x08 ? '3' : '1'));
    #     print_hex(nt.nti.nai.abtUid, nt.nti.nai.szUidLen);
    #     printf("      SAK (SEL_RES): ");
    #     print_hex(&nt.nti.nai.btSak, 1);
    #     if (nt.nti.nai.szAtsLen) {
    #       printf("          ATS (ATR): ");
    #       print_hex(nt.nti.nai.abtAts, nt.nti.nai.szAtsLen);
    #     }
    #   }
    last_id = 0
    import time
    def convert_to_int(whatever):
        value = 0
        for b in whatever:
            value <<= 8
            value |= b
        return value
    while True:
        result = nfc_initiator_select_passive_target(pnd, nmMifare, None, 0, ctypes.byref(nt))
        if (result > 0):
            # might have to do ATQA / SAK / UID / ATS for full ID
            this_id = convert_to_int(nt.nti.nai.abtUid)
            if this_id != last_id:
                print "New tag event:", hex(this_id)
                last_id = this_id
        else:
            print "read fail"
        time.sleep(1)

    nfc_close(pnd)
    nfc_exit(context)

    #   // Close NFC device
    #   nfc_close(pnd);
    #   // Release the context
    #   nfc_exit(context);
    #   exit(EXIT_SUCCESS);
    # }
    #
    # Generated on Mon Feb 24 2014 16:17:57 for libnfc by   doxygen 1.7.6.1
main()
