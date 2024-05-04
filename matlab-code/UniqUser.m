classdef UniqUser < handle
    properties
        id_
        entry
        slot_len
        exit
    end
    
    methods
        function obj = UniqUser(id_, entry_slot, slot_len)
            obj.id_ = id_;
            obj.entry = entry_slot;
            obj.slot_len = slot_len;
            obj.exit = 0;
        end
        
        function processed(obj, exit_slot)
            obj.exit = exit_slot;
        end
        
        function processing_time = get_processing_time(obj)
            processing_time = (obj.exit - obj.entry + 1) * obj.slot_len;
        end
    end
end