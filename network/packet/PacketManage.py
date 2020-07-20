from network.packet.PacketEncryption import *
from network.events.connection.KeepAlive import *
from network.events.connection.CorrectVersion import *
from network.events.connection.ComputerInfo import *
from network.events.connection.Request import *
from network.events.connection.PacketError import *
from network.events.connection.PingMS import *
from network.events.connection.PingUpdate import *
from network.events.connection.PingRequest import *
from network.events.connection.PlayerFPS import *
from network.events.connection.RequestInfo import *
from network.events.connection.PlayerInfo import *
from network.events.connection.PlayerInfo2 import *
from network.events.connection.PlayerInfo3 import *
from network.events.screen.Langue import *
from network.events.screen.Login import *
from network.events.screen.Captcha import *
from network.events.screen.CreateAccount import *
from network.events.screen.ScreenEvents import *
from network.events.chat.Commands import *
from network.events.chat.ChatMessage import *
from network.events.chat.StaffChat import *
from network.events.room.sync.Sync import *
from network.events.room.sync.MouseMovement import *
from network.events.room.sync.Crouch import *
from network.events.room.sync.Mort import *
from network.events.room.sync.ShamanPosition import *
from network.events.room.shaman.ObjectInvocation import *
from network.events.room.shaman.RemoveInvocation import *
from network.events.room.shaman.PlaceObject import *
from network.events.room.shaman.ProjectionSkill import *
from network.events.room.shaman.DemolitionSkill import *
from network.events.room.shaman.GravitationalSkill import *
from network.events.room.shaman.AntigravitySkill import *
from network.events.room.shaman.RestorativeSkill import *
from network.events.room.shaman.HandymouseSkill import *
from network.events.room.shaman.ConvertSkill import *
from network.events.room.shaman.RecyclingSkill import *
from network.events.room.room.GetCheese import *
from network.events.room.room.EnterHole import *
from network.events.room.room.LuaCode import *
from network.events.room.player.Meep import *
from network.events.room.room.EnterRoom import *
from network.events.room.room.RoomPassword import *
from network.events.room.room.Points import *
from network.events.room.room.MusicSend import *
from network.events.room.room.MusicList import *
from network.events.room.room.IceCube import *
from network.events.room.room.BridgeBreak import *
from network.events.room.room.Map26 import *
from network.events.room.room.c100x80 import *
from network.events.room.room.ShamanMessage import *
from network.events.old.OldProtocol import *
from network.events.old.room.Anchors import *
from network.events.old.player.Conjuration import *
from network.events.old.player.ConjurationStart import *
from network.events.old.player.ConjurationEnd import *
from network.events.old.room.EditeurValidate import *
from network.events.old.room.EditeurExit import *
from network.events.old.room.Bombs import *
from network.events.old.room.BombExplode import *
from network.events.old.room.PlaceBalloon import *
from network.events.old.room.RemoveBalloon import *
from network.events.old.room.DrawClear import *
from network.events.old.room.Drawing import *
from network.events.old.room.DrawPoints import *
from network.events.old.room.MoveCheese import *
from network.events.player.RoomsList import *
from network.events.player.BuySkill import *
from network.events.player.Emote import *
from network.events.player.Emotions import *
from network.events.player.RedistributeSkills import *
from network.events.player.TransformationObject import *
from network.events.player.PlayerVampire import *
from network.events.player.PlayerReport import *
from network.events.player.ShamanFly import *
from network.events.player.ShamanType import *
from network.events.player.ChangeShamanColor import *
from network.events.room.player.Transformation import *
from network.events.shop.ShopList import *
from network.events.shop.ShopInfos import *
from network.events.shop.ShopBuyMouseItem import *
from network.events.shop.ShopEquip import *
from network.events.shop.ShopCustomItem import *
from network.events.shop.ShopBuyCustomItem import *
from network.events.shop.ShopBuyShamanItem import *
from network.events.shop.ShopEquipShamanItem import *
from network.events.shop.ShopBuyCustomShamanItem import *
from network.events.shop.ShopCustomShamanItem import *
from network.events.shop.ShopBuyFraises import *
from network.events.shop.ShopBuyClothe import *
from network.events.shop.ShopSaveClothe import *
from network.events.shop.ShopEquipClothe import *
from network.events.inventory.InventoryOpen import *
from network.events.inventory.EquipConsumable import *
from network.events.inventory.UseConsumable import *
from network.events.tribulle.Tribulle import *
from network.events.tribulle.player.ChangeGender import *
from network.events.tribulle.friends.FriendsList import *
from network.events.tribulle.friends.FriendsClosed import *
from network.events.tribulle.friends.FriendsAdd import *
from network.events.tribulle.friends.FriendsRemove import *
from network.events.tribulle.ignoreds.IgnoredsList import *
from network.events.tribulle.ignoreds.IgnoredsAdd import *
from network.events.tribulle.ignoreds.IgnoredsRemove import *
from network.events.tribulle.marriage.MarriagePropose import *
from network.events.tribulle.marriage.MarriageAnswer import *
from network.events.tribulle.marriage.MarriageDivorce import *
from network.events.tribulle.chat.ChatWhisper import *
from network.events.tribulle.chat.ChatSilence import *
from network.events.tribulle.chat.ChatJoin import *
from network.events.tribulle.chat.ChatQuem import *
from network.events.tribulle.chat.ChatMessage import *
from network.events.tribulle.chat.ChatLeave import *
from network.events.modopwet.Modopwet import *
from network.events.modopwet.ModopwetLangue import *
from network.events.modopwet.ModopwetFollow import *
from network.events.modopwet.ModopwetBan import *
from network.events.modopwet.ModopwetNotification import *
from network.events.modopwet.ModopwetDelete import *
from network.events.modopwet.ChatLog import *
from network.events.missions.MissionsOpen import *
from network.packet.ByteArray import *

class PacketManage:
	def __init__(self, users):
		self.users = users

		self.packetEncryption = PacketEncryption(self, users)

		self.packets = {}
		self.oldPackets = {}
		self.tribullePackets = {}

		self.registry(CorrectVersion)
		self.registry(KeepAlive)
		self.registry(Langue)
		self.registry(ComputerInfo)
		self.registry(Request)
		self.registry(PacketError)
		self.registry(PingMS)
		self.registry(PingUpdate)
		self.registry(PingRequest)
		self.registry(PlayerFPS)
		self.registry(RequestInfo)
		self.registry(PlayerInfo)
		self.registry(PlayerInfo2)
		self.registry(PlayerInfo3)
		self.registry(Login)
		self.registry(PCaptcha)
		self.registry(CreateAccount)
		self.registry(ScreenEvents)
		self.registry(RCommands)
		self.registry(ChatMessage)
		self.registry(MouseMovement)
		self.registry(Crouch)
		self.registry(ShamanPosition)
		self.registry(ObjectInvocation)
		self.registry(RemoveInvocation)
		self.registry(Mort)
		self.registry(GetCheese)
		self.registry(EnterHole)
		self.registry(RoomsList)
		self.registry(EnterRoom)
		self.registry(RoomPassword)
		self.registry(PlaceObject)
		self.registry(ProjectionSkill)
		self.registry(DemolitionSkill)
		self.registry(GravitationalSkill)
		self.registry(AntigravitySkill)
		self.registry(RestorativeSkill)
		self.registry(HandymouseSkill)
		self.registry(ConvertSkill)
		self.registry(RecyclingSkill)
		self.registry(Meep)
		self.registry(Points)
		self.registry(BuySkill)
		self.registry(Emote)
		self.registry(Emotions)
		self.registry(MusicSend)
		self.registry(MusicList)
		self.registry(ShopList)
		self.registry(ShopInfos)
		self.registry(ShopBuyMouseItem)
		self.registry(ShopEquip)
		self.registry(ShopBuyCustomItem)
		self.registry(ShopCustomItem)
		self.registry(ShopBuyShamanItem)
		self.registry(ShopEquipShamanItem)
		self.registry(ShopBuyCustomShamanItem)
		self.registry(ShopCustomShamanItem)
		self.registry(ShopBuyFraises)
		self.registry(ShopBuyClothe)
		self.registry(ShopSaveClothe)
		self.registry(ShopEquipClothe)
		self.registry(Transformation)
		self.registry(RedistributeSkills)
		self.registry(Tribulle)
		self.registry(OldProtocol)
		self.registry(PlayerVampire)
		self.registry(PlayerReport)
		self.registry(Modopwet)
		self.registry(ModopwetLangue)
		self.registry(ModopwetFollow)
		self.registry(ModopwetBan)
		self.registry(ModopwetNotification)
		self.registry(ModopwetDelete)
		self.registry(ChatLog)
		self.registry(LuaCode)
		self.registry(Sync)
		self.registry(IceCube)
		self.registry(BridgeBreak)
		self.registry(Map26)
		self.registry(StaffChat)
		self.registry(c100x80)
		self.registry(ShamanMessage)
		self.registry(ShamanFly)
		self.registry(ShamanType)
		self.registry(ChangeShamanColor)
		self.registry(InventoryOpen)
		self.registry(EquipConsumable)
		self.registry(UseConsumable)
		self.registry(MissionsOpen)
		
		self.registryOld(Anchors)
		self.registryOld(Conjuration)
		self.registryOld(ConjurationStart)
		self.registryOld(ConjurationEnd)
		self.registryOld(TransformationObject)
		self.registryOld(EditeurExit)
		self.registryOld(EditeurValidate)
		self.registryOld(Bombs)
		self.registryOld(BombExplode)
		self.registryOld(RemoveBalloon)
		self.registryOld(PlaceBalloon)
		self.registryOld(Drawing)
		self.registryOld(DrawClear)
		self.registryOld(DrawPoints)
		self.registryOld(MoveCheese)

		self.registryTribulle(ChangeGender)
		self.registryTribulle(FriendsList)
		self.registryTribulle(FriendsClosed)
		self.registryTribulle(FriendsAdd)
		self.registryTribulle(FriendsRemove)
		self.registryTribulle(IgnoredsList)
		self.registryTribulle(IgnoredsAdd)
		self.registryTribulle(IgnoredsRemove)
		self.registryTribulle(MarriagePropose)
		self.registryTribulle(MarriageAnswer)
		self.registryTribulle(MarriageDivorce)
		self.registryTribulle(ChatWhisper)
		self.registryTribulle(ChatSilence)
		self.registryTribulle(ChatJoin)
		self.registryTribulle(ChatQuem)
		self.registryTribulle(TChatMessage)
		self.registryTribulle(ChatLeave)

		if int(users.server.config["debug"]):
			self.users.server.println("Packets loaded: {}".format(len(self.packets)), "debug")

	def decrypt(self, packetID, packet, keys):
		data = ByteArray()
		while packet.bytesAvailable():
			packetID = (packetID + 1) % len(keys)
			data.writeByte(packet.readByte() ^ keys[packetID])
		return data

	def registry(self, packet):
		self.packets[(packet.C << 8) | packet.CC] = packet

	def registryOld(self, packet):
		self.oldPackets[(packet.C << 8) | packet.CC] = packet

	def registryTribulle(self, packet):
		self.tribullePackets[packet.code] = packet