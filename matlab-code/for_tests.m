clc;
close all;

% Определение параметров
amplitudes = [1, 2, 3, 4]; % Различные амплитуды
frequencies = [1, 5, 10];

% if any(amplitudes == 1)
%     disp("YES!")
% end
% 
% disp(1 * 0.33 * exp(-1 * 0.33))
% 
% if 13 <= 2
%     tmp = 5;
% else
%     tmp = 9;
% end
% disp(tmp)

% [max_throughput, index] = find_max_throughput(frequencies);
% % max_throughput = output(1);
% % index = output(2);
% 
% disp(max_throughput)
% disp(index)
% disp(prod(factorial(amplitudes)))


% m = 2;
% l = 3;
% 
% % Generate all combinations of indices
% indices = cell(1, l);
% for i = 1:l
%     indices{i} = 0:m;
% end
% 
% disp(indices)
% 
% % Create a grid of indices
% [indices{:}] = ndgrid(indices{:});
% 
% disp(ndgrid(indices{:}))
% 
% % Concatenate the indices into a single matrix
% combinations = reshape(cat(l+1, indices{:}), [], l);
% 
% disp(combinations);

l = 3;
m = 2;

% Generate all combinations of indices
indices = cell(1, l);
for i = 1:l
    indices{i} = 0:m;
end

% Create a grid of indices
[indices{:}] = ndgrid(indices{:});
%disp(ndgrid(indices{:}))

% Concatenate the indices into a single matrix
combinations = cat(l+1, indices{:});

% Reshape the matrix to have one combination per row
combinations = reshape(combinations, [], l);

% Display the combinations
%disp(combinations);

for i = 1:length(frequencies)
    % Цикл для отрисовки синусоид с разными амплитудами
    figure;
    hold on;
    for j = 1:length(amplitudes)
        plot_sin_with_amplitude(frequencies(i), amplitudes(j));
    end
    hold off;
    legend; % Отображение легенды
    xlabel('Time'); % Подпись оси X
    ylabel('Amplitude'); % Подпись оси Y
    title_str = sprintf('Sinusoids with different amplitudes & frequence %2.f', frequencies(i));
    title(title_str); % Заголовок
end

combinations = generate_combinations2(m, l);
[~, num_combs] = size(combinations);
disp(num_combs)
for i = 1:num_combs
    disp(sum(combinations{i}))
    % users_in_channels = combinations{1}(i);
    % disp(sum(users_in_channels))
end

function plot_sin_with_amplitude(frequence, amplitude)
    num_samples = 100; % Количество выборок
    t = linspace(0, 2*pi, num_samples); % Временной интервал от 0 до 2*pi
    y = amplitude * sin(frequence * t); % Формирование синусоиды с заданной амплитудой
    plot(t, y, 'DisplayName', ['Amplitude = ', num2str(amplitude)]); % Отображение синусоиды
end

function [max_throughput, index] = find_max_throughput(throughputs)
    max_throughput = 0.0;
    index = 1;
    for i = 1:length(throughputs)
        if throughputs(i) > max_throughput
            max_throughput = throughputs(i);
            index = i;
        end
    end
end

function combinations = generate_combinations(m, l)
    function result = generate_combinations_helper(curr_combination, depth)
        if depth == l
            result = {curr_combination};
            return;
        end
        
        result = {};
        for num = 0:m
            curr_combination{end+1} = num;
            result = [result, generate_combinations_helper(curr_combination, depth + 1)];
            curr_combination(end) = [];
        end
    end

    initial_combination = {};
    combinations = generate_combinations_helper(initial_combination, 0);
end


function combinations = generate_combinations1(m, l)
    function result = generate_combinations_helper(curr_combination, depth)
        if depth == l
            result = curr_combination;
            return;
        end
        
        result = [];
        for num = 0:m
            result = [result; generate_combinations_helper([curr_combination, num], depth + 1)];
        end
    end

    initial_combination = [];
    combinations = generate_combinations_helper(initial_combination, 0);
end

function combinations = generate_combinations2(m, l)
    function result = generate_combinations_helper(curr_combination, depth)
        if depth == l
            result = {curr_combination};
            return;
        end
        
        result = {};
        for num = 0:m
            new_combination = [curr_combination, num];
            result = [result, generate_combinations_helper(new_combination, depth + 1)];
        end
    end

    initial_combination = [];
    combinations = generate_combinations_helper(initial_combination, 0);
end

