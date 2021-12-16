import math

# Input data and samples data
input = "E20D4100AA9C0199CA6A3D9D6352294D47B3AC6A4335FBE3FDD251003873657600B46F8DC600AE80273CCD2D5028B6600AF802B2959524B727D8A8CC3CCEEF3497188C017A005466DAA6FDB3A96D5944C014C006865D5A7255D79926F5E69200A164C1A65E26C867DDE7D7E4794FE72F3100C0159A42952A7008A6A5C189BCD456442E4A0A46008580273ADB3AD1224E600ACD37E802200084C1083F1540010E8D105A371802D3B845A0090E4BD59DE0E52FFC659A5EBE99AC2B7004A3ECC7E58814492C4E2918023379DA96006EC0008545B84B1B00010F8E915E1E20087D3D0E577B1C9A4C93DD233E2ECF65265D800031D97C8ACCCDDE74A64BD4CC284E401444B05F802B3711695C65BCC010A004067D2E7C4208A803F23B139B9470D7333B71240050A20042236C6A834600C4568F5048801098B90B626B00155271573008A4C7A71662848821001093CB4A009C77874200FCE6E7391049EB509FE3E910421924D3006C40198BB11E2A8803B1AE2A4431007A15C6E8F26009E002A725A5292D294FED5500C7170038C00E602A8CC00D60259D008B140201DC00C401B05400E201608804D45003C00393600B94400970020C00F6002127128C0129CDC7B4F46C91A0084E7C6648DC000DC89D341B23B8D95C802D09453A0069263D8219DF680E339003032A6F30F126780002CC333005E8035400042635C578A8200DC198890AA46F394B29C4016A4960C70017D99D7E8AF309CC014FCFDFB0FE0DA490A6F9D490010567A3780549539ED49167BA47338FAAC1F3005255AEC01200043A3E46C84E200CC4E895114C011C0054A522592912C9C8FDE10005D8164026C70066C200C4618BD074401E8C90E23ACDFE5642700A6672D73F285644B237E8CCCCB77738A0801A3CFED364B823334C46303496C940"
samples = [
    "D2FE28",
    "38006F45291200",
    "EE00D40C823060",
    "8A004A801A8002F478",
    "620080001611562C8802118E34",
    "C0015000016115A2E0802F182340",
    "A0016C880162017C3686B18A3D4780"
]

# Lookup table for quick and easy decoding of hex. Puzzles seem to exclusively use upper case.
hex_lookup = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}

# Take a hex string and turn it into a binary string
def hex_to_binary(hex_input):
    binary_output = ""
    for c in hex_input:
        binary_output = binary_output + hex_lookup[c]
    return binary_output

# Python can convert binary to decimal, which makes this easy
def binary_to_decimal(binary_input):
    return int(binary_input, 2)

# Grab the next bits_wanted bits from the binary input and return them together with the new pos
def walk_forward(binary_input, pos, bits_wanted, as_binary=False):
    if as_binary:
        return((pos+bits_wanted, binary_input[pos:pos+bits_wanted]))
    else:
        return((pos+bits_wanted, binary_to_decimal(binary_input[pos:pos+bits_wanted])))

# Parse position is the point in the binary_input we've got up to
def decode_packet(binary_input, parse_position, max_bits_to_decode = -1):
    # A list of values from this packet
    packet_type = -1
    packet_values = list()

    # Remember where we started so that we can see how mnay bits we've decoded
    started_at = parse_position

    # Get the packet version and packet type
    (parse_position, packet_version) = walk_forward(binary_input, parse_position, 3)
    (parse_position, packet_type) = walk_forward(binary_input, parse_position, 3)

    # How we parse the rest depends on the packet type
    if(packet_type == 4):
        # This is a literal value

        # Grab pieces of the literal value in chunks of 5 bits
        more_to_come = "1"
        literal_value = ""
        while(more_to_come == "1"):
            (parse_position, more_to_come) = walk_forward(binary_input, parse_position, 1, as_binary=True)
            (parse_position, number_fragment) = walk_forward(binary_input, parse_position, 4, as_binary=True)
            literal_value = literal_value + number_fragment     # Assemble the fragments into the final binary value

        # Decode the literal value and set the computed_packet_value so that it is returned at the end of the function
        computed_packet_value = binary_to_decimal(literal_value)

    else:
        # This is an operator packet

        # Read 1 bit indicating which kind of subpacket reads we will do
        (parse_position, length_type_id) = walk_forward(binary_input, parse_position, 1)

        if(length_type_id == 0):
            # The next 15 bits are the total length in bits of the sub packets
            (parse_position, subpackets_total_length) = walk_forward(binary_input, parse_position, 15)

            # Go and get the subpackets
            destination_parse_position = parse_position + subpackets_total_length
            while parse_position < destination_parse_position:
                (parse_position, value) = decode_packet(binary_input, parse_position, subpackets_total_length)
                packet_values.append(value)         # Build a list of subpacket return values
        else:
            # The next 11 bits are the number of sub-packets immediately contained
            (parse_position, subpackets_count) = walk_forward(binary_input, parse_position, 11)
            for i in range(0, subpackets_count):
                (parse_position, value) = decode_packet(binary_input, parse_position)
                packet_values.append(value)         # Build a list of subpacket return values

        # Calculate the computed value of this packet based on the operator type abd the list of subpacket values
        if packet_type == 0:
            computed_packet_value = sum(packet_values)
        elif packet_type == 1:
            computed_packet_value = math.prod(packet_values)
        elif packet_type == 2:
            packet_values.sort()
            computed_packet_value = packet_values[0]
        elif packet_type == 3:
            packet_values.sort()
            computed_packet_value = packet_values[-1]
        elif packet_type == 5:
            computed_packet_value = 1 if packet_values[0] > packet_values[1] else 0
        elif packet_type == 6:
            computed_packet_value = 1 if packet_values[0] < packet_values[1] else 0
        elif packet_type == 7:
            computed_packet_value = 1 if packet_values[0] == packet_values[1] else 0

    # Return the computed value of this packet
    return((parse_position, computed_packet_value))

# Running for real - 
# NOTE: This assumes there is always 1 single outer packet that contains all others. 
# If there was a list of packets this would only read and evaluate the first one.
(parse_position, value) = decode_packet(hex_to_binary(input), 0)
print("Solution: ", value)
