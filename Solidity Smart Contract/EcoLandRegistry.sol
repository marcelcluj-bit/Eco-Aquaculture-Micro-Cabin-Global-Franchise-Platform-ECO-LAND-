// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

/**
 * @title EcoLandSPVRegistry
 * @dev Manages fractional 1-Hectare micro-parcels (20 plots of 5 Ares) with cabin ownership and franchise royalty routing.
 */
contract EcoLandSPVRegistry is ERC721, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _parcelIds;

    struct ParcelInfo {
        uint256 siteId;
        string region;
        uint256 plotAreaAres; // 5 Ares
        bool cabinIncluded;
        uint256 salePriceWei;
        bool isSold;
    }

    mapping(uint256 => ParcelInfo) public parcels;
    mapping(uint256 => address) public siteTreasury;

    event ParcelRegistered(uint256 indexed parcelId, uint256 indexed siteId, string region);
    event ParcelSold(uint256 indexed parcelId, address indexed buyer, uint256 price);
    event RoyaltyDistributed(uint256 indexed siteId, uint256 protocolFee);

    constructor() ERC721("EcoLandSPVPlot", "ELP") Ownable(msg.sender) {}

    /**
     * @dev Register a new batch of 20 parcels for a 1-Hectare site.
     */
    function batchRegisterSiteParcels(
        uint256 siteId,
        string memory region,
        uint256 pricePerPlotWei,
        address treasuryAddress
    ) external onlyOwner {
        siteTreasury[siteId] = treasuryAddress;
        
        for (uint256 i = 0; i < 20; i++) {
            _parcelIds.increment();
            uint256 newParcelId = _parcelIds.current();

            parcels[newParcelId] = ParcelInfo({
                siteId: siteId,
                region: region,
                plotAreaAres: 5,
                cabinIncluded: true,
                salePriceWei: pricePerPlotWei,
                isSold: false
            });

            emit ParcelRegistered(newParcelId, siteId, region);
        }
    }

    /**
     * @dev Purchase a parcel with automatic 5% protocol fee routing.
     */
    function buyParcel(uint256 parcelId) external payable {
        ParcelInfo storage parcel = parcels[parcelId];
        require(!parcel.isSold, "Parcel already sold");
        require(msg.value >= parcel.salePriceWei, "Insufficient funds");

        parcel.isSold = true;

        // Calculate 5% protocol royalty fee
        uint256 protocolFee = (msg.value * 5) / 100;
        uint256 siteOwnerShare = msg.value - protocolFee;

        // Transfer to site treasury / DAO
        address treasury = siteTreasury[parcel.siteId];
        (bool successTreasury, ) = payable(treasury).call{value: siteOwnerShare}("");
        require(successTreasury, "Transfer to treasury failed");

        // Mint NFT representing deed / micro-cabin plot ownership
        _safeMint(msg.sender, parcelId);

        emit ParcelSold(parcelId, msg.sender, msg.value);
        emit RoyaltyDistributed(parcel.siteId, protocolFee);
    }
}
