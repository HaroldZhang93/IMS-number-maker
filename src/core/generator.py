#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
IMS号码脚本生成器核心模块
"""

class ScriptGenerator:
    """脚本生成器类，用于生成IMS号码放号脚本"""
    
    def __init__(self):
        """初始化生成器"""
        self.templates = {
            'uspp_pvi': 'ADD NEWPVI:PVITYPE=0,PVI={phone}@{domain},IREGFLAG=1,IDENTITYTYPE=0,PECFN={cfn},SECFN={cfn},PCCFN={cfn},SCCFN={cfn},SecVer=30,UserName=,PASSWORD={password},Realm={domain},ACCTypeList=*,ACCInfoList=*,ACCValueList=*;',
            'uspp_pui_sip': 'ADD NEWPUI:IDENTITYTYPE=0,PUI=sip:{phone}@{domain},BARFLAG=0,REGAUTHFG=1,SIFCIDList={sifc_id},ROAMSCHEMEID=1,SPID=1,SPDesc=65535,PVIList={phone}@{domain},SCSCFNameList=sip:{scscf}.{domain},LOOSEROUTEIND=0;',
            'uspp_pui_tel': 'ADD NEWPUI:IDENTITYTYPE=0,PUI=tel:{phone},BARFLAG=0,REGAUTHFG=1,SIFCIDList={sifc_id},ROAMSCHEMEID=1,SPID=1,SPDesc=65535,PVIList={phone}@{domain},SCSCFNameList=sip:{scscf}.{domain},LOOSEROUTEIND=0;',
            'uspp_impregset': 'SET IMPREGSET:PUIList=sip:{phone}@{domain}$tel:{phone},DefaultPUI=tel:{phone};',
            'uspp_aliasegroup': 'SET ALIASEGROUP:PUIList=sip:{phone}@{domain}$tel:{phone},AliasGroupID={alias_id};',
            'enum_naptr': 'ADD NaptrRec:name={reversed_number}.e164.arpa,Order=0,Preference=1,Flags=U,Service=sip+e2u,Regexp=!^.*$!sip:{phone}@{domain}!,TTL=0;',
            'sss_osu_sbr': 'ADD OSU SBR:PUI="tel:{phone}",NETTYPE=1,CC={cc},LATA={lata},TYPE="IMS",OFFLCHG="ON",CORHT="LC"&"DDD"&"IDD"&"SPCS"&"HF"&"HKMACAOTW"&"LT",CIRHT="LC"&"DDD"&"IDD"&"SPCS"&"HF"&"HKMACAOTW"&"LT",CTXOUTRHT="GRPIN"&"GRPOUT"&"GRPOUTNUM",CTXINRHT="GRPIN"&"GRPOUT"&"GRPOUTNUM"IMSUSERTYPE="NMIMS";',
            'sss_osu_oip': 'SET OSU OIP:PUI="sip:{phone}@{domain}",NF="TEL";'
        }
    
    def _reverse_number_for_enum(self, number):
        """将电话号码反转为ENUM格式
        
        Args:
            number: 电话号码，如 +861088889001
            
        Returns:
            反转后的号码，如 1.0.0.9.8.8.8.8.0.1.6.8
        """
        # 去掉前缀 +
        if number.startswith('+'):
            number = number[1:]
        
        # 反转并用点分隔
        return '.'.join(reversed(number))
    
    def _extract_alias_id(self, phone):
        """从电话号码提取别名ID
        
        Args:
            phone: 电话号码，如 +861088889001
            
        Returns:
            别名ID，如 861088889001
        """
        if phone.startswith('+'):
            return phone[1:]
        return phone
    
    def generate_uspp_script(self, phone_numbers, params):
        """生成USPP网元放号脚本
        
        Args:
            phone_numbers: 电话号码列表
            params: 参数字典，包含domain, cfn, password, sifc_id, scscf等
            
        Returns:
            生成的USPP脚本
        """
        script_parts = ["//******************************USPP网元放号********************************************************"]
        
        # 生成PVI部分
        for phone in phone_numbers:
            script_parts.append(self.templates['uspp_pvi'].format(
                phone=phone,
                domain=params['domain'],
                cfn=params['cfn'],
                password=params['password']
            ))
        
        script_parts.append("\n")
        
        # 生成SIP PUI部分
        for phone in phone_numbers:
            script_parts.append(self.templates['uspp_pui_sip'].format(
                phone=phone,
                domain=params['domain'],
                sifc_id=params['sifc_id'],
                scscf=params['scscf']
            ))
        
        script_parts.append("\n")
        
        # 生成TEL PUI部分
        for phone in phone_numbers:
            script_parts.append(self.templates['uspp_pui_tel'].format(
                phone=phone,
                domain=params['domain'],
                sifc_id=params['sifc_id'],
                scscf=params['scscf']
            ))
        
        script_parts.append("\n")
        
        # 生成IMPREGSET部分
        for phone in phone_numbers:
            script_parts.append(self.templates['uspp_impregset'].format(
                phone=phone,
                domain=params['domain']
            ))
        
        script_parts.append("\n")
        
        # 生成ALIASEGROUP部分
        for phone in phone_numbers:
            script_parts.append(self.templates['uspp_aliasegroup'].format(
                phone=phone,
                domain=params['domain'],
                alias_id=self._extract_alias_id(phone)
            ))
        
        return "\n".join(script_parts)
    
    def generate_enum_script(self, phone_numbers, params):
        """生成ENUM网元放号脚本
        
        Args:
            phone_numbers: 电话号码列表
            params: 参数字典，包含domain等
            
        Returns:
            生成的ENUM脚本
        """
        script_parts = ["\n\n//******************************ENUM网元放号********************************************************\n"]
        
        for phone in phone_numbers:
            reversed_number = self._reverse_number_for_enum(phone)
            script_parts.append(self.templates['enum_naptr'].format(
                reversed_number=reversed_number,
                phone=phone,
                domain=params['domain']
            ))
        
        return "\n".join(script_parts)
    
    def generate_sss_script(self, phone_numbers, params):
        """生成SSS网元放号脚本
        
        Args:
            phone_numbers: 电话号码列表
            params: 参数字典，包含cc, lata, domain等
            
        Returns:
            生成的SSS脚本
        """
        script_parts = ["\n\n\n//******************************SSS网元放号********************************************************"]
        
        # 生成OSU SBR部分
        for phone in phone_numbers:
            script_parts.append(self.templates['sss_osu_sbr'].format(
                phone=phone,
                cc=params['cc'],
                lata=params['lata']
            ))
        
        script_parts.append("\n")
        
        # 生成OSU OIP部分
        for phone in phone_numbers:
            script_parts.append(self.templates['sss_osu_oip'].format(
                phone=phone,
                domain=params['domain']
            ))
        
        return "\n".join(script_parts)
    
    def generate_full_script(self, start_number, count, params):
        """生成完整的放号脚本
        
        Args:
            start_number: 起始号码，如 +861088889001
            count: 号码数量
            params: 参数字典
            
        Returns:
            完整的放号脚本
        """
        # 生成号码列表
        phone_numbers = []
        
        # 解析起始号码
        prefix = ""
        number_part = ""
        
        if start_number.startswith('+'):
            prefix = '+'
            number_part = start_number[1:]
        else:
            number_part = start_number
        
        # 找到数字部分的起始位置
        base_number = int(number_part)
        
        # 生成号码列表
        for i in range(count):
            current_number = base_number + i
            phone_numbers.append(f"{prefix}{current_number}")
        
        # 生成各部分脚本
        uspp_script = self.generate_uspp_script(phone_numbers, params)
        enum_script = self.generate_enum_script(phone_numbers, params)
        sss_script = self.generate_sss_script(phone_numbers, params)
        
        # 合并完整脚本
        return uspp_script + enum_script + sss_script 