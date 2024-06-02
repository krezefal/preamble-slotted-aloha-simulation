clc;
close all;

%% CONSTS
% SIM CONSTANTS

SLOTS = 2000;

CH_NUM = 1:2;

DTP_LEN = 1;
MIN_EP_LEN = 0;
MAX_EP_LEN = 1;
EP_LEN_STEP = 0.5;
% SLOTS_LEN is EP_LEN with DTP_LEN
SLOTS_LEN = DTP_LEN+MIN_EP_LEN:EP_LEN_STEP:DTP_LEN+MAX_EP_LEN;

MAX_LAMBD = 2;
LAMBD_STEP = 0.01;
LAMBDAS = 0:LAMBD_STEP:MAX_LAMBD;

% PROG CONSTANTS
ROUNDING = '%.4f';
SAVE_PATH = strcat('../graphs/matlab');


%% SIMULATING T(λ)

for i = 1:length(CH_NUM)
    ch_num = CH_NUM(i);
    fprintf('КОЛ-ВО КАНАЛОВ = %d:\n', ch_num);

    lambda_out = zeros(length(SLOTS_LEN), length(LAMBDAS));
    lambda_in = zeros(length(SLOTS_LEN), length(LAMBDAS));
    avg_delays = zeros(length(SLOTS_LEN), length(LAMBDAS));
    for j = 1:length(SLOTS_LEN)
        slot_len = SLOTS_LEN(j);
        format_str = sprintf(['Итерация моделирования #%d: длина окна ' ...
            '= %s (ФИ=%s, ФП=%s)\n'], j, ROUNDING, ROUNDING, ROUNDING);
        fprintf(format_str, slot_len, slot_len-DTP_LEN, DTP_LEN);

        for k = 1:length(LAMBDAS)
            lambda = LAMBDAS(k);
            if lambda == 0
                lambda = 0.0001;
            end
            % format_str = sprintf('======( λ = %s )======\n', ROUNDING);
            % fprintf(format_str, lambda);

            [lambda_in(j, k), lambda_out(j, k), avg_delays(j, k)] = ...
                run_simulation(lambda, slot_len, ch_num, SLOTS);
        end
    end

    % Plotting T(λ) sim
    figure;
    hold on;
    for j = 1:length(SLOTS_LEN)
        plot(LAMBDAS, lambda_out(j, :));
    end

    hold off;
    legendEntries = cell(length(SLOTS_LEN), 1);
    for j = 1:length(SLOTS_LEN)
        legendEntries{j} = sprintf('Длина окна = %.4f', SLOTS_LEN(j));
    end
    
    legend(legendEntries, 'Location', 'southeast');
    xlabel('Интенсивность вх. потока');
    ylabel('T(λ)');
    xlim('auto')
    ylim('auto')
    title_str = sprintf(['Зависимость пропускной способности от ' ...
        'интенсивности вх. потока\n(моделирование, кол-во ' ...
        'каналов %d)'], ch_num);
    title(title_str);
    filename = sprintf('/%dch_lambd_step_%.4f_slots_%d_throughput_sim', ...
        ch_num, LAMBD_STEP, SLOTS);
    savefig([SAVE_PATH, filename, '.fig']);
    saveas(gcf, [SAVE_PATH, filename, '.png']);

    % Plotting delay sim
    figure;
    hold on;
    for j = 1:length(SLOTS_LEN)
        plot(LAMBDAS, avg_delays(j, :));
    end

    hold off;
    legendEntries = cell(length(SLOTS_LEN), 1);
    for j = 1:length(SLOTS_LEN)
        legendEntries{j} = sprintf('Длина окна = %.4f', SLOTS_LEN(j));
    end
    
    legend(legendEntries, 'Location', 'southeast');
    xlabel('Интенсивность вх. потока');
    ylabel('Задержка');
    xlim('auto')
    ylim([0, 20]);
    title_str = sprintf(['Зависимость задержки от ' ...
        'интенсивности вх. потока\n(моделирование, кол-во ' ...
        'каналов %d)'], ch_num);
    title(title_str);
    filename = sprintf('/%dch_lambd_step_%.4f_slots_%d_delay_sim', ...
        ch_num, LAMBD_STEP, SLOTS);
    savefig([SAVE_PATH, filename, '.fig']);
    saveas(gcf, [SAVE_PATH, filename, '.png']);
end


function [lambda_in, lambda_out, avg_delay] = ...
    run_simulation(lambda, slot_len, ch_num, slots)

    % Generate stream
    poisson_dist = zeros(1, slots);
    cur_timestamp = 0.0;
    timestamps = [];
    
    while true
        dt = ((-1 / lambda) * (log(rand())));
        cur_timestamp = cur_timestamp + dt;
        if cur_timestamp > (slots - 1) * slot_len
            break;
        end
        
        timestamps = [timestamps, cur_timestamp];
    end

    if numel(timestamps) == 0
        lambda_in = 0.0;
        lambda_out = 0.0;
        avg_delay = 0.0;
        return
    end

    for t = timestamps
        slot_num = ceil(t / slot_len);
        poisson_dist(slot_num) = poisson_dist(slot_num) + 1;
    end

    % disp("ВРЕМЕННЫЕ МЕТКИ:");
    % disp(timestamps);
    % disp("АКТИВНОСТЬ АБОНЕНТОВ ПО СЛОТАМ (длина слота = " + slot_len + "):");
    % disp(poisson_dist);

    % Init runtime data
    id_counter = 0;
    active_users = containers.Map('KeyType', 'int64', 'ValueType', 'any');
    sent_data_packets = [];
    
    % Run simulation
    for cur_slot = 1:slots
        % Update active users list
        for i = 1:poisson_dist(cur_slot)
            id_counter = id_counter + 1;
            active_users(id_counter) = UniqUser(id_counter, cur_slot, ...
                slot_len);
        end

        if isempty(active_users)
            continue
        end

        % Exploration phase
        % EP: active users choosing channels
        ch_situation = containers.Map('KeyType', 'int32', 'ValueType', 'any');
        for num = 1:ch_num
            ch_situation(num) = [];
        end

        P_ep = min(1, ch_num / length(active_users));
        for user_cell = values(active_users)
            if rand() < P_ep
                user = user_cell{1};
                channel = randi(ch_num);
                ch_situation(channel) = [ch_situation(channel), user];
            end
        end

        users_in_channels = 0;
        users_cell = values(ch_situation);
        for i = 1:numel(users_cell)
            users_in_channels = users_in_channels + numel(users_cell{i});
        end

        if users_in_channels == 0
            continue
        end
        
        % EP: split active users who decide to transmit a preamble into 2 
        % groups
        group_success = containers.Map('KeyType', 'int32', 'ValueType', 'any');
        group_conflict = containers.Map('KeyType', 'int32', 'ValueType', 'any');
        
        for channel = keys(ch_situation)
            cur_users_arr = ch_situation(channel{1});
            if numel(cur_users_arr) == 1
                contention_free_user = cur_users_arr(1);
                group_success(channel{1}) = contention_free_user;
            else
                group_conflict(channel{1}) = cur_users_arr;
            end
        end

        % Data transmission phase
        for channel = keys(group_success)
            % ALWAYS SUCCESS
            contention_free_user = group_success(channel{1});
            active_users.remove(contention_free_user.id_);
            contention_free_user.processed(cur_slot);
            sent_data_packets = [sent_data_packets, contention_free_user];
        end
        
        users_in_contention = 0;
        users_cell = values(group_conflict);
        for i = 1:numel(users_cell)
            users_in_contention = ...
                users_in_contention + numel(users_cell{i});
        end

        if users_in_contention ~= 0
            % EP: users from a confict group reselect channels from this 
            % group
            empty_instance = UniqUser(-1, -1, 0);
            users_in_contention_arr = ...
                repmat(empty_instance, 1, users_in_contention);
            idx = 1;
            for channel = keys(group_conflict)
                cur_users_arr = group_conflict(channel{1});
                for i = 1:numel(cur_users_arr)
                    user = cur_users_arr(i);
                    users_in_contention_arr(idx) = user;
                    idx = idx + 1;
                end
                group_conflict(channel{1}) = [];
            end
            
            for user = users_in_contention_arr
                channels = keys(group_conflict);
                idx = randi(length(channels));
                new_channel = channels{idx};
                group_conflict(new_channel) = ...
                    [group_conflict(new_channel), user];
            end

            for channel = keys(group_conflict)
                cur_users_arr = group_conflict(channel{1});
                if ~isempty(cur_users_arr)
                    active_users_decisions = containers.Map('KeyType', ...
                        'int64', 'ValueType', 'logical');
    
                    P_dtp = ...
                        min(1, (ch_num - length(group_success)) / ...
                            users_in_contention);
    
                    for i = 1:numel(cur_users_arr)
                        user = cur_users_arr(i);
                        active_users_decisions(user.id_) = rand() < P_dtp;
                    end
                    
                    if all(cellfun(@(x) ~x, values(active_users_decisions)))
                        % EMPTY
                        continue;
                    else
                        if sum(cellfun(@(x) x == true, ...
                                values(active_users_decisions))) == 1
                            % SUCCESS
                            for user_id_cell = keys(active_users_decisions)
                                user_id = user_id_cell{1};
                                decision = active_users_decisions(user_id);
                                if decision == true
                                    user = active_users(user_id);
                                    active_users.remove(user_id);
                                    user.processed(cur_slot);
                                    sent_data_packets = ...
                                        [sent_data_packets, user];
                                    break;
                                end
                            end
                        else
                            % CONFLICT
                            continue;
                        end
                    end
                end
            end
        end
    end

    % Calculate system params
    total_time = timestamps(end);
    lambda_in = ...
        (length(sent_data_packets) + length(active_users)) / total_time;
    lambda_out = length(sent_data_packets) / total_time;
    if ~isempty(sent_data_packets)
        overall_delay = 0.0;
        for i = 1:length(sent_data_packets)
            overall_delay = ...
                overall_delay + sent_data_packets(i).get_processing_time();
        end
        avg_delay = overall_delay / length(sent_data_packets);
    else
        avg_delay = 0.0;
    end
end

