PAGE_SIZE = 1024

PAGE_TABLE = {
    0: 5,
    1: 2,
    2: 9,
    3: 1
}

SEGMENT_TABLE = {
    0: (1000, 400),
    1: (2200, 300),
    2: (500, 150)
}


# ============================================================
# PAGING
# ============================================================

def translate_paged_address(logical_address):
    page_number = logical_address // PAGE_SIZE
    offset = logical_address % PAGE_SIZE

    if page_number not in PAGE_TABLE:
        return {
            "status": "PAGE FAULT",
            "logical_address": logical_address,
            "page": page_number,
            "offset": offset
        }

    frame_number = PAGE_TABLE[page_number]

    physical_address = (
        frame_number * PAGE_SIZE + offset
    )

    return {
        "status": "SUCCESS",
        "logical_address": logical_address,
        "page": page_number,
        "offset": offset,
        "frame": frame_number,
        "physical_address": physical_address
    }


# ============================================================
# SEGMENTATION
# ============================================================

def translate_segmented_address(segment, offset):

    if segment not in SEGMENT_TABLE:
        return {
            "status": "SEGMENTATION FAULT",
            "segment": segment,
            "offset": offset
        }

    base, limit = SEGMENT_TABLE[segment]

    if offset >= limit:
        return {
            "status": "SEGMENTATION FAULT",
            "segment": segment,
            "offset": offset,
            "base": base,
            "limit": limit
        }

    physical_address = base + offset

    return {
        "status": "SUCCESS",
        "segment": segment,
        "offset": offset,
        "base": base,
        "limit": limit,
        "physical_address": physical_address
    }


# ============================================================
# OUTPUT
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("TASK 7 — PAGING AND SEGMENTATION ADDRESS TRANSLATION")
    print("=" * 70)

    # --------------------------------------------------------
    # Paging
    # --------------------------------------------------------

    print("\n" + "-" * 70)
    print("PAGING")
    print("-" * 70)

    paged_addresses = [260, 1500, 3000, 5000]

    expected_paged = {
        260: 5380,
        1500: 2524,
        3000: 10168
    }

    paging_pass = True

    for logical_address in paged_addresses:

        result = translate_paged_address(logical_address)

        if result["status"] == "PAGE FAULT":
            print(
                f"Logical address {logical_address}: "
                f"PAGE FAULT "
                f"(page {result['page']} not in page table)"
            )
            continue

        print(
            f"Logical address {logical_address}: "
            f"page={result['page']}, "
            f"offset={result['offset']}, "
            f"frame={result['frame']}, "
            f"physical address={result['physical_address']}"
        )

        if result["physical_address"] != expected_paged[logical_address]:
            paging_pass = False

    # --------------------------------------------------------
    # Segmentation
    # --------------------------------------------------------

    print("\n" + "-" * 70)
    print("SEGMENTATION")
    print("-" * 70)

    segmented_addresses = [
        (0, 150),
        (1, 350),
        (2, 100)
    ]

    expected_segmented = {
        (0, 150): 1150,
        (2, 100): 600
    }

    segmentation_pass = True

    for segment, offset in segmented_addresses:

        result = translate_segmented_address(
            segment,
            offset
        )

        if result["status"] == "SEGMENTATION FAULT":
            print(
                f"Logical address ({segment}, {offset}): "
                f"SEGMENTATION FAULT"
            )
            continue

        print(
            f"Logical address ({segment}, {offset}): "
            f"base={result['base']}, "
            f"limit={result['limit']}, "
            f"physical address={result['physical_address']}"
        )

        if result["physical_address"] != expected_segmented[
            (segment, offset)
        ]:
            segmentation_pass = False

    # --------------------------------------------------------
    # Acceptance check
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("TASK 7 ACCEPTANCE CHECK")
    print("=" * 70)

    paging_results = [
        translate_paged_address(address)
        for address in paged_addresses
    ]

    segmentation_results = [
        translate_segmented_address(segment, offset)
        for segment, offset in segmented_addresses
    ]

    required_paging_ok = (
        paging_results[0].get("physical_address") == 5380
        and paging_results[1].get("physical_address") == 2524
        and paging_results[2].get("physical_address") == 10168
        and paging_results[3]["status"] == "PAGE FAULT"
    )

    required_segmentation_ok = (
        segmentation_results[0].get("physical_address") == 1150
        and segmentation_results[1]["status"] == "SEGMENTATION FAULT"
        and segmentation_results[2].get("physical_address") == 600
    )

    if required_paging_ok and required_segmentation_ok:
        print(
            "PASS: Paging and segmentation acceptance criteria satisfied."
        )
    else:
        print(
            "FAIL: Paging and segmentation acceptance criteria not satisfied."
        )